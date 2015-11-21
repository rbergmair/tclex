__all__ \
  = [ "ENWiktionaryTextParser",
      "enwiktionary_convert_category",
      "enwiktionary_de_word_bymeta",
      "enwiktionary_en_word_bymeta",
      "enwiktionary_en_word_bycontent" ];

from bz2 import BZ2File;

from xml.sax.saxutils import escape;


from txcrunch.wikimedia.wm.mw import MediawikiMetadataTreewalker;
from txcrunch.wikimedia.wm.mw import MediawikiPagesXMLParser;
from txcrunch.wikimedia.wm.mw import MediawikiWikitextParser;



class ENWiktionaryTextParser( MediawikiWikitextParser ):


  EN_POSs \
    = [ "en-abbr", # . . . . . . .  0
        "en-acronym",  # . . . . .  1
        "en-adj",  # . . . . . . .  2
        "en-adv",  # . . . . . . .  3
        "en-con",  # . . . . . . .  4
        "en-cont", # . . . . . . .  5
        "en-det",  # . . . . . . .  6
        "en-initialism", # . . . .  7
        "en-interj", # . . . . . .  8
        "en-noun", # . . . . . . .  9
        "en-plural noun",  # . . . 10
        "en-part", # . . . . . . . 11
        "en-phrase", # . . . . . . 12
        "en-prefix", # . . . . . . 13
        "en-prep", # . . . . . . . 14
        "en-PP", # . . . . . . . . 15
        "en-pron", # . . . . . . . 16
        "en-proper noun",  # . . . 17
        "en-proverb",  # . . . . . 18
        "en-punctuation mark", # . 19
        "en-suffix", # . . . . . . 20
        "en-symbol", # . . . . . . 21
        "en-verb"  # . . . . . . . 22
      ];

  DE_POSs \
    = [ "de-abbreviation", # . . .  0 
        "de-acronym",  # . . . . .  1
        "de-adv",  # . . . . . . .  2
        "de-adj",  # . . . . . . .  3
        "de-prep", # . . . . . . .  4
        "de-pron", # . . . . . . .  5
        "de-verb-strong",  # . . .  6
        "de-verb-weak",  # . . . .  7
        "de-diacritical mark", # .  8
        "de-initialism", # . . . .  9
        "de-letter", # . . . . . . 10
        "de-noun", # . . . . . . . 11
        "de-phrase", # . . . . . . 12
        "de-proper noun",  # . . . 13
        "de-proverb",  # . . . . . 14
        "de-punctuation mark", # . 15
        "de-verb", # . . . . . . . 16
        "de-verb form",  # . . . . 17
        "de-verb-irregular"  # . . 18
      ];   
  
  DE_NOUN \
    = ( [],
        [ ( "g",    True,  True ),
          ( "g2",   False, True ),
          ( "pl",   False, True ),
          ( "pl2",  False, True ),
          ( "dim",  False, True ),
          ( "gen",  False, True ),
          ( "gen2", False, True ),
          ( "f",    False, True ),
          ( "m",    False, True ),
          ( "g1",        False, False ),
          ( "gen1",      False, False ),
          ( "genitive",  False, False ),
          ( "genitive2", False, False ),
          ( "pl1",       False, False ),
          ( "plural",    False, False ),
          ( "plural2",   False, False ) ],
        lambda x: x );
  
  
  def __init__( self, outdir, affix ):

    MediawikiWikitextParser.__init__( self );
    self._outdir = outdir;
    self._affix = affix;
  
  
  def __enter__( self ):
    
    assert MediawikiWikitextParser.__enter__( self ) is self;

    self._de_other \
      = open(
            self._outdir \
              + "/enwiktionary{}_de_other.csv".format( self._affix ),
            "wt"
          );

    self._de_verb \
      = open(
            self._outdir \
              + "/enwiktionary{}_de_verb.csv".format( self._affix ),
            "wt"
          );

    self._de_noun \
      = open(
            self._outdir \
              + "/enwiktionary{}_de_noun.csv".format( self._affix ),
            "wt"
          );
    
    self._de_adj \
      = open(
            self._outdir \
              + "/enwiktionary{}_de_adj.csv".format( self._affix ),
            "wt"
          );

    self._en_verb_regular \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_verb_regular.csv".format( self._affix ),
            "wt"
          );

    self._en_verb_irregular \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_verb_irregular.csv".format( self._affix ),
            "wt"
          );

    self._en_adv_regular \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_adv_regular.csv".format( self._affix ),
            "wt"
          );

    self._en_adv_irregular \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_adv_irregular.csv".format( self._affix ),
            "wt"
          );

    self._en_noun \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_noun.csv".format( self._affix ),
            "wt"
          );

    self._en_adj_regular \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_adj_regular.csv".format( self._affix ),
            "wt"
          );

    self._en_adj_irregular \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_adj_irregular.csv".format( self._affix ),
            "wt"
          );

    self._en_other \
      = open(
            self._outdir \
              + "/enwiktionary{}_en_other.csv".format( self._affix ),
            "wt"
          );
    
    return self;
  
  
  def __exit__( self, exc_type, exc_value, traceback ):

    self._de_other.close();
    
    self._de_verb.close();
    self._de_adj.close();
    self._de_noun.close();
    
    self._en_other.close();

    self._en_adj_irregular.close();
    self._en_adj_regular.close();
    
    self._en_noun.close();

    self._en_adv_irregular.close();
    self._en_adv_regular.close();
    
    self._en_verb_irregular.close();
    self._en_verb_regular.close();

    return \
      MediawikiWikitextParser.__exit__(
          self, exc_type, exc_value, traceback
        );  
  
  
  def __call__( self, title, txt ):
    
    return MediawikiWikitextParser.__call__( self, title, txt );
  
  
  def process_wikifunc( self, func, args, kwargs ):
    
    rslt = False;
    
    if self._title.find( ":" ) != -1 or self._title.find( "/" ) != -1:
      return rslt;

    if func in [ "en-adv", "en-adj" ]:
      
      if func == "en-adv":
        outf_regular = self._en_adv_regular;
        outf_irregular = self._en_adv_irregular;
      
      else:
        outf_regular = self._en_adj_regular;
        outf_irregular = self._en_adj_irregular;
      
      p = 0;
      if len(args) > 0 and args[0] == "-":
        args = args[1:];
        self._to_csv( outf_regular, [ self._id, "-", 0, self._id ] );
        p = -1;
      
      if "pos" in kwargs:
        
        print( "WARNING! ignoring funky shit on " + self._id );
        self._warnings += 1;
    
      elif len(args) == 0:
        
        self._to_csv( outf_regular, [ self._id, "mm", p, self._id ] );
      
      elif len(args) == 1 and args[-1] == "er":

        self._to_csv( outf_regular, [ self._id, "er", p, self._id ] );

      elif len(args) == 2 and args[-1] == "er":

        self._to_csv( outf_regular, [ self._id, "er", p, args[0] ] );

      elif len(args) == 1 and args[-1] == "ier":

        self._to_csv( outf_regular, [ self._id, "ier", p, self._id ] );

      elif len(args) == 2 and args[-1] == "ier":

        self._to_csv( outf_regular, [ self._id, "ier", p, args[0] ] );

      elif len(args) == 1 and args[-1] == "-":

        self._to_csv( outf_regular, [ self._id, "-", p, self._id ] );
      
      elif len(args) == 2 and args[0] == "er" and args[1] == "more":

        self._to_csv( outf_regular, [ self._id, "mm", p, self._id ] );
        self._to_csv( outf_regular, [ self._id, "er", p, self._id ] );
      
      elif len(args) == 2:
        
        args0 = args[0];
        args1 = args[1];
        
        if args0 == "more":
          args0 = "more "+self._id;
        elif args0 == "er":
          args0 = self._id+"er";
        elif args0 == "ier":
          args0 = self._id+"ier";
        
        if args1 == "most":
          args1 = "most "+self._id;
        elif args1 == "est":
          args0 = self._id+"est";
        elif args1 == "iest":
          args0 = self._id+"iest";

        self._to_csv( outf_irregular, [ self._id, args0, args1 ] );
      
      elif len(args) == 1:

        args0 = args[0];
        if args0 == "more":
          args0 = "more "+self._id;
        elif args0 == "er":
          args0 = self._id+"er";
        elif args0 == "ier":
          args0 = self._id+"ier";

        self._to_csv( outf_irregular, [ self._id, args0, "most "+self._id ] );
      
      else:
      
        print(
            "WARNING! {} unknown parameters {}".format( self._id, repr(args) )
          );
        self._warnings += 1;

    # return;

    elif func in [ "de-verb-strong", "de-verb-weak", "de-verb-irregular" ]:
      
      vtype = None;
      if func == "de-verb-strong":
        vtype = "s";
      elif func == "de-verb-weak":
        vtype = "w";
      elif func == "de-verb-irregular":
        vtype = "x";
      
      aux = "haben";
      if "auxiliary" in kwargs:
        aux = kwargs[ "auxiliary" ];
      if len(args) == 4:
        aux = args[-1];
        args = args[:-1];
      
      if len(args) != 3:
        print( "{}: WARNING! wrong verb {}".format( self._id, args ) );
        self._warnings += 1;

      else:
        self._to_csv(
            self._de_verb,
            [ self._id, vtype, args[0], args[1], args[2], aux ]
          );


    elif func == "de-decl-adj":
      
      comp = None;
      sup = None;
      if len(args) >= 1:
        comp = args[0];
      if len(args) >= 2:
        sup = None;
      
      if "comparative" in kwargs:
        if comp:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        comp = kwargs[ "comparative" ];

      if "superlative" in kwargs:
        if sup:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        sup = kwargs[ "superlative" ];

        self._to_csv( self._de_adj, [ self._id, comp, sup ] );


    elif func == "de-noun":
      
      if "genitive" in kwargs:
        if "gen" in kwargs or "gen1" in kwargs:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        kwargs[ "gen" ] = kwargs[ "genitive" ];
      
      if "gen1" in kwargs:
        if "gen" in kwargs or "genitive" in kwargs:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        kwargs[ "gen" ] = kwargs[ "gen1" ];

      if "genitive2" in kwargs:
        if "gen2" in kwargs:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        kwargs[ "gen2" ] = kwargs[ "genitive2" ];

      if "plural" in kwargs:
        if "pl" in kwargs or "pl1" in kwargs:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        kwargs[ "pl" ] = kwargs[ "plural" ];
      
      if "pl1" in kwargs:
        if "pl" in kwargs or "plural" in kwargs:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        kwargs[ "pl" ] = kwargs[ "pl1" ];

      if "plural2" in kwargs:
        if "pl2" in kwargs:
          print( "{}: WARNING! {} rewrite clash".format( self._id, args ) );
          self._warnings += 1;
        kwargs[ "pl2" ] = kwargs[ "plural2" ];
    
      for r in self.process_template( self.DE_NOUN, args, kwargs ):
        rslt = True;
        self._to_csv( self._de_noun, r );


    elif func in self.DE_POSs:
      
      self._to_csv( self._de_other, [ self._id, self.DE_POSs.index(func) ] );

    
    elif func in [ "en-noun", "en-proper noun" ]:
      
      sg = kwargs.get( "sg" );
      pl = kwargs.get( "pl" );
      
      ntype = None;
      if func == "en-proper noun":
        ntype = "P";
      
      def warn_plural_specified():
        print( self._title, args, kwargs );
        print( "WARNING! plural of absolute specified" );
        self._warnings += 1;
  
      def warn_plural_respecified():
        print( self._title, args, kwargs );
        print( "WARNING! plural specified twice" );
        self._warnings += 1;
      
      def process_args_basic( args, p ):
      
        if len(args) == 0:
          self._to_csv(
              self._en_noun,
              [ self._id, ntype, p, sg or self._id, self._id+"s" ]
            );
        
        elif args[-1] in [ "s", "es", "ies" ]:
          
          if len(args) == 1:
            warn_plural_respecified() if pl else None;
            self._to_csv(
                self._en_noun,
                [ self._id, ntype, p, sg or self._id, self._id+args[-1] ]
              );
          
          elif len(args) == 2:
            warn_plural_respecified() if pl else None;
            self._to_csv(
                self._en_noun,
                [ self._id, ntype, p, sg or self._id, args[0]+args[-1] ]
              );
            
        elif len(args) == 1 and args[-1] == "-":
          
          warn_plural_specified() if pl else None;
          self._to_csv(
              self._en_noun,
              [ self._id, ntype, p, sg or self._id, None ]
            );
  
        elif len(args) == 1:

          warn_plural_specified() if pl and args[0] else None;
          self._to_csv(
              self._en_noun,
              [ self._id, ntype, p, sg or self._id, args[0] ]
            );

        else:
          print( self._title, args, kwargs );
          print( "WARNING! unknown pattern".format(args) );
          self._warnings += 1;
      
      if ("!" in args) or ("?" in args):

        warn_plural_specified() if pl else None;
        self._to_csv(
            self._en_noun,
            [ self._id, ntype, 0, sg or self._id, None ]
          );
      
      elif len(args) >= 2 and args[0] == "-":

        process_args_basic( ["-"], 0 );
        process_args_basic( args[1:], -1 );
      
      elif len(args) >= 2 and args[-1] == "-": 

        process_args_basic( args[:-1], 0 );
        process_args_basic( ["-"], -1 );
      
      else:

        process_args_basic( args, 0 );

      if pl:
        self._to_csv(
            self._en_noun,
            [ self._id, ntype, sg or self._id, 0, pl ]
          );
      
      if "pl2" in kwargs:
        self._to_csv(
            self._en_noun,
            [ self._id, ntype, sg or self._id, -1, kwargs["pl2"] ]
          );
        
    
    elif func == "en-verb":
      
      if len(args) == 0:
      
        self._to_csv(
            self._en_verb_regular,
            [ self._id, "s", self._id, None ]
          );

      else:
        
        if args[-1] in [ "s", "es", "d", "ed", "ing" ]:
          
          if len(args) == 2:
            self._to_csv(
                self._en_verb_regular,
                [ self._id, args[1], args[0], None ]
              );

          elif len(args) == 3:
            self._to_csv(
                self._en_verb_regular,
                [ self._id, args[2], args[0], args[1] ]
              );

          else:

            print(
                self._title,
                args
              );

            print(
                "WARNING! {} parameters to en-verb[{}]"\
                 .format( len(args), args[-1] )
              );

            self._warnings += 1;
        
        else:
          
          if len(args) == 3:
            self._to_csv(
                self._en_verb_irregular,
                [ self._id, args[0], args[1], args[2], args[2] ]
              );

          elif len(args) == 4:
            self._to_csv(
                self._en_verb_irregular,
                [ self._id, args[0], args[1], args[2], args[3] ]
              );

          else:

            print(
                self._title,
                args
              );

            print(
                "WARNING! {} parameters to en-verb[irreg]"\
                 .format( len(args), args[-1] )
              );

            self._warnings += 1;
    
    
    elif func in self.EN_POSs:
      
      self._to_csv( self._en_other, [ self._id, self.EN_POSs.index(func) ] );



def enwiktionary_convert_category( f, root, pos ):

  conn_args = [ "localhost", "enwiktionary", "root", "" ];

  with MediawikiMetadataTreewalker( *conn_args ) as r:

    pages \
      = r.page_by_category(
            r.subcat_pageids_trans_closure( root )
          );

    for ( page_title, catid ) in pages:
      page_title \
        = page_title.replace( "_", " " ).replace( "|", "" );
      f.write( page_title + "|" + pos + "|" + str(catid) + "\n" )



def enwiktionary_en_word_bymeta( out_fn ):

  MAP \
    = [ #
        ( "English_verbs", "v" ),
        ( "English_nouns", "n" ),
        ( "English_adjectives", "a" ),
        ( "English_adverbs", "r" ),
        #    
        ( "English_articles", "x" ),
        ( "English_conjunctions", "x" ),
        ( "English_determiners", "x" ),
        ( "English_interjections", "x" ),
        ( "English_numerals", "x" ),
        ( "English_particles", "x" ),
        ( "English_postpositions", "x" ),
        ( "English_prepositions", "x" ),
        ( "English_pronouns", "x" ),
        ( "English_non-constituents", "x" ),
        ( "English_phrases", "x" ),
        ( "English_proverbs", "x" ),
        ( "English_abbreviations", "x" ) ];

  with open( out_fn, "wt" ) as f:

    for ( title, pos ) in MAP:
      enwiktionary_convert_category( f, title, pos );



def enwiktionary_de_word_bymeta( out_fn ):

  MAP \
    = [ #
        ( "German_verbs", "v" ),
        ( "German_nouns", "n" ),
        ( "German_adjectives", "a" ),
        ( "German_adverbs", "r" ),    
        #
        ( "German_articles", "x" ),
        ( "German_conjunctions", "x" ),
        ( "German_interjections", "x" ),
        ( "German_numerals", "x" ),
        ( "German_particles", "x" ),
        ( "German_prepositions", "x" ),
        ( "German_pronouns", "x" ) ];

  with open( out_fn, "wt" ) as f:

    for ( title, pos ) in MAP:
      enwiktionary_convert_category( f, title, pos );



def enwiktionary_en_word_bycontent( in_fn, out_dirn ):

  w = 0;
  with BZ2File( in_fn, "rb" ) as f:
    with MediawikiPagesXMLParser() as xmlp:
      with ENWiktionaryTextParser( out_dirn, "" ) as txtp:
        xmlp( f, txtp );
        w += txtp.warnings;

  return w;
