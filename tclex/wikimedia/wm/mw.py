__all__ \
  = [ "MediawikiMetadataTreewalker",
      "MediawikiPagesXMLParser",
      "MediawikiWikitextParser" ];

from re import fullmatch as re_fullmatch;

from html.parser import HTMLParser;

from xml.sax import make_parser;
from xml.sax.handler import ContentHandler;
from xml.sax.handler import feature_external_ges, feature_external_pes;



class MediawikiMetadataTreewalker:
  
  
  def __init__( self, host, database, user, password ):

    self._host = host;
    self._database = database;
    self._user = user;
    self._password = password;

    self._db = None;


  def __enter__( self ):

    import mysql.connector;

    self._db \
      = mysql.connector.Connect(
            host = self._host,
            database = self._database,
            user = self._user,
            password = self._password
          );

    self._db.set_autocommit( True );

    return self;

  def __exit__( self, exc_type, exc_value, traceback ):

    self._db.close();
    self._db = None;

  
  def subcat_pageids_trans_closure( self, root_title, circuit_breaker=100 ):
    
    ids = set();
    
    cur = self._db.cursor();
    try:
      
      cur.execute(
          """
            SELECT page_id
              FROM page
             WHERE page_namespace = 14
               AND page_title = '{}'
             LIMIT 50
          """\
           .format(root_title)
        );
      
      for (page_id,) in cur:
        ids.add( page_id );
      
    finally:
      cur.close();
    
    if len( ids ) != 1:
      print( "WARNING! {} doesn't exist".format(root_title) )
      return set();
    
    for i in range( 0, circuit_breaker+1 ): #@UnusedVariable

      assert i < circuit_breaker;      
  
      len_before = len(ids);
  
      cur = self._db.cursor();
      try:
        
        cur.execute(
            """
              SELECT c.cl_from
                FROM page AS p,
                     categorylinks AS c
               WHERE p.page_title = c.cl_to
                 AND p.page_namespace = 14
                 AND p.page_id IN ({})
                 AND c.cl_type = 'subcat'
            """\
             .format( repr(ids)[1:-1] )
          );
        
        for (page_id,) in cur:
          ids.add( page_id );
        
      finally:
        cur.close();
      
      if len(ids) <= len_before:
        break;
      
    return ids;
  
  
  def page_by_category( self, category_pageids, flds="p.page_title" ):
    
    if not category_pageids:
      return;
    
    cats = set();
    
    catid_by_title = {};

    cur = self._db.cursor();
    try:
      
      cur.execute(
          """
            SELECT p.page_title, p.page_id
              FROM page AS p
             WHERE p.page_id IN ({})
          """\
           .format( repr(category_pageids)[1:-1] )
        );

      for (page_title,page_id) in cur:
        catid_by_title[ page_title ] = page_id;
        cats.add( page_title.decode( "utf-8" ) );
      
    finally:
      cur.close();

    cur = self._db.cursor();
    try:
      
      cur.execute(
          """
          SELECT {}, c.cl_to
            FROM page AS p,
                 categorylinks AS c
           WHERE p.page_id = c.cl_from
             AND c.cl_type = 'page'
             AND c.cl_to IN ({})
             AND p.page_namespace = 0
          """\
           .format( flds, repr(cats)[1:-1] )
        );

      for record in cur:
        record_ = ();
        for r in record[:-1]:
          if isinstance( r, bytes ):
            record_ += ( r.decode( "utf-8" ), );
          else:
            record_ += ( r, );
        record_ += ( catid_by_title[ record[-1] ], );
        yield record_;
      
    finally:
      cur.close();
  
  
  def page_title_by_id( self, ids ):

    if not ids:
      return;
    
    cur = self._db.cursor();
    try:

      cur.execute(
          """
            SELECT p.page_id, p.page_title
              FROM page AS p
             WHERE p.page_id IN ({})
          """\
           .format( repr(ids)[1:-1] )
        );
      
      return \
        dict(
            [ ( id_,
                t.decode( "utf-8" ) if isinstance( t, bytes ) else t ) \
              for ( id_, t ) in cur ]
          );
    
    finally:
      cur.close();



class MediawikiPagesXMLParser( ContentHandler ):


  def __init__( self ):

    pass;


  def __enter__( self ):

    self._txt = "";

    return self;

  def __exit__( self, exc_type, exc_value, traceback ):

    pass;


  def __call__( self, f, txtp ):

    self._txtp = txtp;

    parser = make_parser();
    parser.setFeature( feature_external_ges, 0 );
    parser.setFeature( feature_external_pes, 0 );
    parser.setContentHandler( self );

    while True:

      rslt = f.read( 10240 );
      if not rslt:
        break;
      parser.feed( rslt );


  def startElement( self, name, attrs ):

    self._txt = "";

    if name == "page":
      self._title = "";

  def characters( self, txt ):

    self._txt += txt;

  def endElement( self, name ):

    if name == "title":
      self._title = self._txt;

    if name == "text":
      self._txtp( self._title, self._txt );



class MediawikiWikitextParser:


  def __init__( self ):

    self._html_parser = HTMLParser();


  def __enter__( self ):

    self._warnings = 0;
    return self;

  def __exit__( self, exc_type, exc_value, traceback ):

    pass;


  @property
  def warnings( self ):
    return self._warnings;


  def __call__( self, title, txt ):

    self._title = title;
    self._id = self._title;

    first_lbrace = False;
    first_rbrace = False;

    reading = False;

    reading_tag = False;

    tx = "";

    tag = "";

    rslt = False;

    for ch in txt:

      if ch == "<":
        reading_tag = True;
        tag = "";
        continue;

      if reading_tag:
        if ch == ">":
          reading_tag = False;
          if tag in [ "br", "br ", "br/", "br /" ]:
            ch = ";";
        else:
          tag += ch;

      if reading_tag:
        continue;

      if ch == "{":
        if first_lbrace:
          reading  = True;
          tx = "";
        else:
          first_lbrace = True;
        continue;
      else:
        first_lbrace = False;

      if not reading:
        continue;

      if ch == "}":
        if first_rbrace:
          reading = False;
          r = self.process_dblbrace( tx );
          rslt = rslt or r;
        else:
          first_rbrace = True;
        continue;
      else:
        first_rbrace = False;

      tx += ch;

    if not rslt:
      self.process_catchall();


  def process_dblbrace( self, txt ):

    items = [];
    for tx in txt.split("|"):
      items.append( tx.replace("\n","").strip() );

    if len( items ) == 1:
      self.process_wikilink( items[0] );
      return;

    func = items[0];

    args = [];
    kwargs = {};

    for item in items[1:]:

      item_ = item.split("=");
      if len(item_) != 2:
        args.append( item );
      else:
        kwargs[ item_[0].strip() ] = item_[1].strip();

    return self.process_wikifunc( func, args, kwargs );


  def process_wikilink( self, wikilink ):

    pass;


  def process_wikifunc( self, func, args, kwargs ):

    pass;


  def process_template( self, template, args, kwargs ):

    rslt_fixed = [ self._id ];

    ( args_templ, kwargs_templ, map_func ) = template;

    if len(args_templ) > 0:

      if len(args) != len(args_templ):
        print( args );
        print(
            "{}: WARNING! number of fixed args doesn't match template"\
             .format( self._title )
          );
        self._warnings += 1;

      for ( ( is_mandatory, do_reproduce ), val ) in zip( args_templ, args ):

        if is_mandatory and not val:
          print(
              "{}: WARNING! mandatory fixed argument not supplied"\
               .format( self._title )
            );
          self._warnings += 1;

        if do_reproduce:
          rslt_fixed.append( val );

    suffices = [];
    for suffix in [ "", " 1", " 2", " 3", " 4" ]:
      for ( field, is_mandatory, do_reproduce ) in kwargs_templ:
        if do_reproduce:
          if field+suffix in kwargs and not suffix in suffices:
            suffices.append( suffix );

    kwfields = set();

    for suffix in suffices:

      rslt_kw = [];

      for ( field, is_mandatory, do_reproduce ) in kwargs_templ:

        field_ = field + suffix;

        kwfields.add( field_ );

        matched_val_ = None;
        for key in kwargs:
          if re_fullmatch( field_, key ):
            matched_val_ = kwargs[ key ];

        matched_val = None;
        for key in kwargs:
          if re_fullmatch( field, key ):
            matched_val = kwargs[ key ];

        if is_mandatory and ( suffix != "" or suffices  == [""] ):
          if matched_val_ is None and matched_val is None:            
            print(
                "{}: WARNING! mandatory field {} missing"\
                 .format( self._title, field )
              );
            self._warnings += 1;

        if do_reproduce:
          if matched_val_ is not None:
            rslt_kw.append( matched_val_ );
          elif matched_val is not None:
            rslt_kw.append( matched_val );
          else:
            rslt_kw.append( None );

      yield map_func( rslt_fixed + rslt_kw );

    for key in kwargs:

      matched = False;
      for field_ in kwfields:
        if re_fullmatch( field_, key ):
          matched = True;

      if not matched and not key.endswith('*'):
        print(
            "{}: WARNING! unknown field '{}' was specified"\
             .format( self._title, key )
          );
        self._warnings += 1;


  def process_catchall( self ):

    pass;


  def _to_csv( self, f, dta ):

    def unescape( r ):

      blowout = 0;
      
      while "&amp;" in r:
        r = r.replace( "&nbsp;", " " );
        r = self._html_parser.unescape( r );
        blowout += 1;
        if blowout > 100:
          break;

      r = r.replace( "&nbsp;", " " );
      r = self._html_parser.unescape( r );
      
      return r.strip();

    def val_to_csv( val ):
      
      if val is None:
        val = "";
      
      if isinstance( val, bool ):
        
        if val:
          val = "1";
        else:
          val = "0";
      
      if not isinstance( val, str ):
        
        val = str( val );
      
      val = val.replace( "\n", " " );
      val = val.replace( "|", "" );
      val = unescape(val);
      
      return val;

    f.write( "|".join( [ val_to_csv(x) for x in dta ] ) + "\n" );
