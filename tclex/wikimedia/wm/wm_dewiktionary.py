__all__ \
  = [ "DEWiktionaryTextParser",
      "dewiktionary_de_word_bymeta",
      "dewiktionary_en_word_bymeta",
      "dewiktionary_de_word_bycontent" ];

from bz2 import BZ2File; #@UnresolvedImport
from gzip import GzipFile;


from txcrunch.wikimedia.wm.mw import MediawikiMetadataTreewalker;
from txcrunch.wikimedia.wm.mw import MediawikiPagesXMLParser;
from txcrunch.wikimedia.wm.mw import MediawikiWikitextParser;



class DEWiktionaryTextParser( MediawikiWikitextParser ):

  
  POSs \
    = [ "Abk\u00fcrzung", # . . . . . . . . . . . . . . . . . . 0  
        "Adjektiv", # . . . . . . . . . . . . . . . . . . . . . 1
          "Absolutadjektiv",  # . . . . . . . . . . . . . . . .   2
          "Partizip", # . . . . . . . . . . . . . . . . . . . .   3
          "Komparativ", # . . . . . . . . . . . . . . . . . . .   4
          "Superlativ", # . . . . . . . . . . . . . . . . . . .   5
        "Adposition", # . . . . . . . . . . . . . . . . . . . . 6
          "Postposition", # . . . . . . . . . . . . . . . . . .   7
          "Pr\u00e4position", # . . . . . . . . . . . . . . . .   8
          "Zirkumposition", # . . . . . . . . . . . . . . . . .   9
        "Adverb", # . . . . . . . . . . . . . . . . . . . . . . 10
          "Fokuspartikel", "Gradpartikel",  # . . . . . . . . .   11, 12
          "Interrogativadverb", # . . . . . . . . . . . . . . .   13
          "Konjunktionaladverb",  # . . . . . . . . . . . . . .   14
          "Modalpartikel",  # . . . . . . . . . . . . . . . . .   15
          "Negationspartikel",  # . . . . . . . . . . . . . . .   16
          "Pronominaladverb",   # . . . . . . . . . . . . . . .   17
        "Affix",  # . . . . . . . . . . . . . . . . . . . . . . 18
          "Gebundenes Lexem", # . . . . . . . . . . . . . . . .   19
          "Grammatisches Affix",  # . . . . . . . . . . . . . .   20
          "Pr\u00e4fix",  # . . . . . . . . . . . . . . . . . .   21
          "Pr\u00e4fixoid",   # . . . . . . . . . . . . . . . .   22
          "Suffix",   # . . . . . . . . . . . . . . . . . . . .   23
          "Suffixoid",  # . . . . . . . . . . . . . . . . . . .   24
          "Ortsnamen-Grundwort",  # . . . . . . . . . . . . . .   25
        "Artikel",  # . . . . . . . . . . . . . . . . . . . . . 26
        "Zeichen",  # . . . . . . . . . . . . . . . . . . . . . 27
          "Buchstabe",  # . . . . . . . . . . . . . . . . . . .   28
          "Satzzeichen",  # . . . . . . . . . . . . . . . . . .   29
          "Zahlzeichen", "Ziffer",  # . . . . . . . . . . . . .   30, 31
        "Konjunktion",  # . . . . . . . . . . . . . . . . . . . 32
        "Kontraktion",  # . . . . . . . . . . . . . . . . . . . 33
        "Numerale", # . . . . . . . . . . . . . . . . . . . . . 34
        "Partikel", # . . . . . . . . . . . . . . . . . . . . . 35
          "Vergleichspartikel", # . . . . . . . . . . . . . . .   36
          "Interjektion", # . . . . . . . . . . . . . . . . . .   37
            "Antwortpartikel",  # . . . . . . . . . . . . . . .     38
            "Gru\u00dfwort", "Gru\u00dfformel", # . . . . . . .     39, 40
          "Onomatopoetikum",  # . . . . . . . . . . . . . . . .   41
          "abtrennbare Verbpartikel", # . . . . . . . . . . . .   42
        "Pronomen", "F\u00fcrwort", # . . . . . . . . . . . . . 43, 44
          "Indefinitpronomen",  # . . . . . . . . . . . . . . .   45,
          "Interrogativpronomen", "Fragef\u00fcrwort",  # . . .   46, 47
          "Demonstrativpronomen", # . . . . . . . . . . . . . .   48
          "Personalpronomen", # . . . . . . . . . . . . . . . .   49
          "Possessivpronomen",  # . . . . . . . . . . . . . . .   50
          "Reflexivpronomen", # . . . . . . . . . . . . . . . .   51
          "Relativpronomen",  # . . . . . . . . . . . . . . . .   52
          "Reziprokpronomen", # . . . . . . . . . . . . . . . .   53
        "Subjunktion",  # . . . . . . . . . . . . . . . . . . . 54
        "Substantiv", # . . . . . . . . . . . . . . . . . . . . 55
          "Eigenname",  # . . . . . . . . . . . . . . . . . . .   56
          "Toponym",  # . . . . . . . . . . . . . . . . . . . .   57
          "Vorname",  # . . . . . . . . . . . . . . . . . . . .   58
          "Nachname", # . . . . . . . . . . . . . . . . . . . .   59
          "Zahlklassifikator",  # . . . . . . . . . . . . . . .   60
          "Singularetantum",  # . . . . . . . . . . . . . . . .   61
          "Pluraletantum",  # . . . . . . . . . . . . . . . . .   62
          "Substantivierter Infinitiv", # . . . . . . . . . . .   63
        "Biologische Nomenklatur",  # . . . . . . . . . . . . . 64
        "Verb", # . . . . . . . . . . . . . . . . . . . . . . . 65
          "Hilfsverb",  # . . . . . . . . . . . . . . . . . . .   66
          "Erweiterter Infinitiv",  # . . . . . . . . . . . . .   67
        "Wortverbindung", # . . . . . . . . . . . . . . . . . . 68
        "Deklinierte Form", # . . . . . . . . . . . . . . . . . 69
        "Konjugierte Form", # . . . . . . . . . . . . . . . . . 70
        "Partizip I", # . . . . . . . . . . . . . . . . . . . . 71
        "Partizip II",  # . . . . . . . . . . . . . . . . . . . 72
        "Sprichwort", # . . . . . . . . . . . . . . . . . . . . 73
        "Redewendung",  # . . . . . . . . . . . . . . . . . . . 74
        "Merkspruch", # . . . . . . . . . . . . . . . . . . . . 75
        "Gefl\u00fcgeltes Wort" # . . . . . . . . . . . . . . . 76
      ];


  DE_N_TABLE \
    = ( [],
        [ ( "Nominativ Singular", True, True ),
          ( "Genitiv Singular", True, True ),
          ( "Dativ Singular", True, True ),
          ( "Akkusativ Singular", True, True ),
          ( "Nominativ Plural", True, True ),
          ( "Genitiv Plural", True, True ),
          ( "Dativ Plural", True, True ),
          ( "Akkusativ Plural", True, True ),
          ( "Bild", False, False ),
          ( "Bildbreite", False, False ),
          ( "Bildbezug", False, False ),
          ( "Bildbeschreibung", False, False ),
          ( "Bild 1", False, False ),
          ( "Bildbreite 1", False, False ),
          ( "Bildbezug 1", False, False ),
          ( "Bildbeschreibung 1", False, False ),
          ( "Bild 2", False, False ),
          ( "Bildbreite 2", False, False ),
          ( "Bildbezug 2", False, False ),
          ( "Bildbeschreibung 2", False, False ),
          ( "Bild 3", False, False ),
          ( "Bildbreite 3", False, False ),
          ( "Bildbezug 3", False, False ),
          ( "Bildbeschreibung 3", False, False ),
          ( "Bild 4", False, False ),
          ( "Bildbreite 4", False, False ),
          ( "Bildbezug 4", False, False ),
          ( "Bildbeschreibung 4", False, False ),
        ],
        lambda x: x );


  DE_A_TABLE \
    = ( [],
        [ ( "Positiv", True, True ),
          ( "Komparativ", False, True ),
          ( "Superlativ", False, True ),
          ( "keine weiteren Formen", False, True )
        ],
        lambda x: x );


  DE_V_TABLE \
    = ( [],
        [ ( 'Pr.sens_ich', True, True ),          
          ( 'Pr.sens_du', True, True ),
          ( 'Pr.sens_er, sie, es', True, True ),
          ( 'Pr.teritum_ich', True, True ),          
          ( 'Pr.teritum_es', False, True ),
          ( "Partizip II", True, True ),
          ( "Partizip II\*", False, True ),
          ( "Konjunktiv II_ich", True, True ),          
          ( "Konjunktiv II_es", False, True ),
          ( "Imperativ Singular", True, True ),          
          ( "Imperativ Plural", True, True ),          
          ( "Hilfsverb", True, True ),          
          ( "Bild", False, False ),
          ( "Bildbreite", False, False ),
          ( "Bildbezug", False, False ),
          ( "Bild 1", False, False ),
          ( "Bildbreite 1", False, False ),
          ( "Bildbezug 1", False, False ),
          ( "Bildbeschreibung 1", False, False ),
          ( "Bild 2", False, False ),
          ( "Bildbreite 2", False, False ),
          ( "Bildbezug 2", False, False ),
          ( "Bildbeschreibung 2", False, False ) ],
        lambda x: x );


  DE_A_DECL \
    = ( [],
        [ ( "Positiv-Stamm", True, True ),
          ( "Komparativ-Stamm", False, True ),
          ( "Komparativ-Stamm-ohne-e", False, True ),
          ( "Superlativ-Stamm", False, True ),
          ( "Superlativ-Stamm-ohne-e", False, True ),
          ( "e-Endung", False, True ),
          ( "Pr\u00e4dikativ", False, True ),
          ( "Positiv", False, True ) ],
        lambda x: x );


  DE_V_UNREGELM \
    = ( [],
        [ ( "1", False, True ), # 1 trennbare Vorsible
          ( "2", True, True ),  # 2 Praesensstamm
          ( "3", True, True ),  # 3 Praeteritum 1
          ( "4", True, True ),  # 4 Stamm Konjunktiv II
          ( "5", True, True ),  # 5 Partizip Perfekt
          ( "6", False, True ),  # 6 Praesensstamm 2. Person Singular
          ( "7", False, True ), # 7
          ( "8", False, True ), # 8
          ( "9", False, True ), # 9
          ( "10", False, True ), # 10
          ( "vp", False, True ),
          ( "zp", False, True ),
          ( "gerund", False, True ),
          ( "Hilfsverb", False, True ),
          ( "Partizip+", False, True ),
        ],
        lambda x: x[0:1] + [ "X" ] + x[1:] );


  DE_V_REFLEXIV_UNTRENNBAR \
    = ( [ # trennbarer Teil = None
          ( True, True ),
          ( True, True ),
          ( False, True ),
          ( True, True ),
          ( True, True ),
          ( True, True ), # Partizip II
        ], [
          ( "zr", False, True ),
          ( "gerund", False, True ),
          ( "Akkusativ", False, True ),
        ],
        lambda x: x[0:1] + [ "RU" ] + [ None ] + x[1:] );


  DE_V_REFLEXIV_TRENNBAR \
    = ( [ ( True, True ), # trennbarer Teil
          ( True, True ),
          ( True, True ),
          ( False, True ),
          ( True, True ),
          ( True, True ),
          ( True, True ), # Partizip II
        ], [
          ( "zr", False, True ),
          ( "gerund", False, True ),
          ( "Akkusativ", False, True ),
        ],
        lambda x: x[0:1] + [ "RT" ] + x[1:] );

  
  DE_V_UNTRENNBAR \
    = ( [ # Erstes Partikel = None,
          # Zweites Partikel = None,
          # Vorsilbe = None,
          ( True, True ),
          ( True, True ),
          ( False, True ),
          ( True, True ),
          ( True, True ),
          ( True, True ), # Partizip II
        ], [
          ( "vp", False, True ),
          ( "zp", False, True ),
          ( "gerund", False, True ),
          ( "haben", False, True ),
          ( "Partizip+", False, True ),
          ( "unregelm\u00e4\u00dfig", False, True )
        ],
        lambda x: x[0:1] + [ "U" ] + [ None, None, None ] + x[1:] );


  DE_V_TRENNBAR \
    = ( [ # Erstes Partikel = None,
          # Zweites Partikel = None,
          ( True, True ), # Vorsilbe
          ( True, True ),
          ( True, True ),
          ( False, True ),
          ( True, True ),
          ( True, True ),
          ( True, True ), # Partizip II
        ], [
          ( "vp", False, True ),
          ( "zp", False, True ),
          ( "gerund", False, True ),
          ( "haben", False, True ),
          # Partizip+ = None,
          # unregelmaeszig = None
        ],
        lambda x: x[0:1] + ["T"] + [ None, None ] + x[1:] + [ None, None ] );


  DE_V_DOPPELT_TRENNBAR \
    = ( [ ( True, True ), # Erstes Partikel
          ( True, True ), # Zweites Partikel
          # Vorsilbe = None
          ( True, True ),
          ( True, True ),
          ( False, True ),
          ( True, True ),
          ( True, True ),
          ( True, True ), # Partizip II
        ], [
          ( "vp", False, True ),
          ( "zp", False, True ),
          ( "gerund", False, True ),
          ( "haben", False, True ),
          # Partizip+ = None,
          # unregelmaeszig = None
        ],
        lambda x: x[0:1] + ["D"] + x[1:3] + [None] + x[3:] + [ None, None ] );



  def __init__( self, outdir, affix ):
    
    MediawikiWikitextParser.__init__( self );
    self._outdir = outdir;
    self._affix = affix;
  
  
  def __enter__( self ):
    
    assert MediawikiWikitextParser.__enter__( self ) is self;

    self._unknown \
      = open(
            self._outdir \
              + "/dewiktionary{}_unknown.csv".format( self._affix ),
            "wt"
          );

    self._en_word \
      = open(
            self._outdir \
              + "/dewiktionary{}_en_word_bylink.csv".format( self._affix ),
            "wt"
          );
    
    self._de_word \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_word_bylink.csv".format( self._affix ),
            "wt"
          );

    self._de_adj_table \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_adj_table.csv".format( self._affix ),
            "wt"
          );

    self._de_adj_decl \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_adj_decl.csv".format( self._affix ),
            "wt"
          );

    self._de_noun_table \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_noun_table.csv".format( self._affix ),
            "wt"
          );
    
    self._de_verb_table \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_verb_table.csv".format( self._affix ),
            "wt"
          );

    self._de_verb_konj_regelm \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_verb_conj_regular.csv".format( self._affix ),
            "wt"
          );

    self._de_verb_konj_reflexiv \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_verb_conj_reflexive.csv".format( self._affix ),
            "wt"
          );

    self._de_verb_konj_unregelm \
      = open(
            self._outdir \
              + "/dewiktionary{}_de_verb_conj_irregular.csv".format( self._affix ),
            "wt"
          );
     
    return self;
  

  def __exit__( self, exc_type, exc_value, traceback ):
    
    self._de_verb_konj_unregelm.close();
    self._de_verb_konj_reflexiv.close();
    self._de_verb_konj_regelm.close();
    self._de_verb_table.close();

    self._de_noun_table.close();
    
    self._de_adj_decl.close();
    self._de_adj_table.close();

    self._de_word.close();

    self._en_word.close();

    self._unknown.close();
    
    return \
      MediawikiWikitextParser.__exit__(
          self, exc_type, exc_value, traceback
        );  
  
  
  def __call__( self, title, txt ):
    
    return MediawikiWikitextParser.__call__( self, title, txt );
  
  
  def _coarse_pos( self, pos ):

    if pos == 69:
      return "n";
    if pos == 70:
      return "v";
    
    if 10 <= pos < 18:
      return "r";
    if 1 <= pos < 6:
      return "a";
    if 71 <= pos <= 72:
      return "a";
    if 55 <= pos <= 55:
      return "n";
    if 65 <= pos < 65:
      return "v";
    
    return "x";
    

  def process_wikifunc( self, func, args, kwargs ):
    
    rslt = False;

    if self._title.find( ":" ) != -1 or self._title.find( "/" ) != -1:
      if not self._title.startswith( "Flexion:" ):
        return rslt;

    if func == "Wortart":
      
      if ( len(args) == 1 ) or ( ( len(args) == 2 ) and ( args[1] == "Deutsch" ) ):
        if args[0] not in self.POSs:
          print( "{}: !! WARNING unknown pos {}".format( self._title, args[0] ) );
        else:
          rslt = True;
          pos = self.POSs.index( args[0] );
          self._to_csv( self._de_word, [ self._id, self._coarse_pos(pos), pos ] );

      if ( len(args) == 2 ) and ( args[1] == "Englisch" ):
        if args[0] not in self.POSs:
          print( "{}: !! WARNING unknown pos {}".format( self._title, args[0] ) );
        else:
          rslt = True;
          pos = self.POSs.index( args[0] );
          self._to_csv( self._en_word, [ self._id, self._coarse_pos(pos), pos ] );

    if func == "Deutsch Substantiv \u00dcbersicht":
      for r in self.process_template( self.DE_N_TABLE, args, kwargs ):
        rslt = True;
        self._to_csv( self._de_noun_table, r );

    if func == "Deutsch Adjektiv \u00dcbersicht":
      for r in self.process_template( self.DE_A_TABLE, args, kwargs ):
        rslt = True;
        self._to_csv( self._de_adj_table, r );

    if func == "Deutsch Verb \u00dcbersicht":
      for r in self.process_template( self.DE_V_TABLE, args, kwargs ):
        rslt = True;
        self._to_csv( self._de_verb_table, r );

    if self._title.startswith( "Flexion:" ):
      self._id = self._title[ len("Flexion:") : ];

      if func == "Deklinationsseite Adjektiv":
        for r in self.process_template( self.DE_A_DECL, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_adj_decl, r );

      if func == "Deutsch Verb unregelm\u00e4\u00dfig":
        for r in self.process_template( self.DE_V_UNREGELM, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_verb_konj_unregelm, r );

      if func == "Deutsch Verb schwach untrennbar reflexiv":
        for r in self.process_template( self.DE_V_REFLEXIV_UNTRENNBAR, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_verb_konj_reflexiv, r );
  
      if func == "Deutsch Verb schwach trennbar reflexiv":
        for r in self.process_template( self.DE_V_REFLEXIV_TRENNBAR, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_verb_konj_reflexiv, r );

      if func == "Deutsch Verb schwach untrennbar":
        for r in self.process_template( self.DE_V_UNTRENNBAR, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_verb_konj_regelm, r );    
  
      if func == "Deutsch Verb schwach trennbar":
        for r in self.process_template( self.DE_V_TRENNBAR, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_verb_konj_regelm, r );
  
      if func == "Deutsch Verb schwach doppelt trennbar":
        for r in self.process_template( self.DE_V_DOPPELT_TRENNBAR, args, kwargs ):
          rslt = True;
          self._to_csv( self._de_verb_konj_regelm, r );


  def process_catchall( self ):

    if self._title.find( ":" ) != -1 or self._title.find( "/" ) != -1:
      return;
    self._to_csv( self._unknown, [ self._title ] );



def dewiktionary_convert_category( f, root, pos ):

  conn_args = [ "localhost", "dewiktionary", "root", "" ];

  with MediawikiMetadataTreewalker( *conn_args ) as r:
    
    pages \
      = r.page_by_category(
            r.subcat_pageids_trans_closure( root )
          );
    
    for ( page_title, catid ) in pages:
      page_title \
        = page_title.replace( "_", " " ).replace( "|", "" );
      f.write( page_title + "|" + pos + "|" + str(catid) + "\n" )



def dewiktionary_xx_word_bymeta( out_fn, lang ):

  MAP \
    = [ #
        ( "Adjektiv_({})", "a" ),
        ( "Partizip_I_({})", "a" ),
        ( "Partizip_II_({})", "a" ),
        ( "Adverb_({})", "r" ),
        ( "Substantiv_({})", "n" ),
        ( "Verb_({})", "v" ),
        #
        ( "Singularetantum_({})", "n" ),
        ( "Pluraletantum_({})", "n" ),
        #
        ( "Komparativ‎_({})", "a" ),
        ( "Superlativ_({})", "a" ),
        ( "Deklinierte_Form_({})", "n" ),
        ( "Konjugierte_Form_({})", "v" ),
        #
        ( "Alte_Schreibweise_({})", "x" ),
        ( "Abk\u00fcrzung_({})", "x" ),
        ( "abtrennbare_Verbpartikel_({})", "x" ),
        ( "Affix_({})", "x" ),
        ( "Antwortpartikel_({})", "x" ),
        ( "Artikel_({})", "x" ),
        ( "Buchstabe_({})", "x" ),
        ( "Eigenname_({})", "x" ),
        ( "Fokuspartikel_({})", "x" ),
        ( "Gebundenes_Lexem_({})", "x" ),
        ( "Gradpartikel_({})", "x" ),
        ( "Gru\u00dfformel_({})", "x" ),
        ( "Hilfsverb_({})", "x" ),
        ( "Homonym_({})", "x" ),
        ( "Interjektion_({})", "x" ),
        ( "Konjunktion_({})", "x" ),
        ( "Kontraktion_({})", "x" ),
        ( "Merkspruch_({})", "x" ),
        ( "Modalpartikel_({})", "x" ),
        ( "Negationspartikel_({})", "x" ),
        ( "Numerale_({})", "x" ),
        ( "Onomatopoetikum_({})", "x" ),
        ( "Ortsnamen-Grundwort_({})", "x" ),
        ( "Partikel_({})", "x" ),
        ( "Postposition_({})", "x" ),
        ( "Pronomen_({})", "x" ),
        ( "Pr\u00e4fix_({})", "x" ),
        ( "Pr\u00e4fixoid_({})", "x" ),
        ( "Pr\u00e4position_({})", "x" ),
        ( "Redewendung_({})", "x" ),
        ( "Satzzeichen_({})", "x" ),
        ( "Schweizer_und_Liechtensteiner_Schreibweise", "x" ),
        ( "Sprichwort_({})", "x" ),
        ( "Subjunktion_({})", "x" ),
        ( "Suffix_({})", "x" ),
        ( "Suffixoid_({})", "x" ),
        ( "Vergleichspartikel_({})", "x" ),
        ( "Wortverbindung_({})", "x" ),
        ( "Zahlklassifikator_({})", "x" ),
        ( "Zahlzeichen_({})", "x" ) ];

  with open( out_fn, "wt" ) as f:

    for ( title, pos ) in MAP:
      dewiktionary_convert_category(
          f,
          title.format( lang ),
          pos
        );



def dewiktionary_de_word_bymeta( out_fn ):

  return dewiktionary_xx_word_bymeta( out_fn, "Deutsch" );



def dewiktionary_en_word_bymeta( out_fn ):

  return dewiktionary_xx_word_bymeta( out_fn, "Englisch" );



def dewiktionary_de_word_bycontent( in_fn, out_dirn ):

  w = 0;
  with BZ2File( in_fn, "rb" ) as f:
    with MediawikiPagesXMLParser() as xmlp:
      with DEWiktionaryTextParser( out_dirn, "" ) as txtp:
        xmlp( f, txtp );
        w += txtp.warnings;
  
  return w;
