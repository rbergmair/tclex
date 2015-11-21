from os.path import isfile;
from os import remove;

from txcrunch.wikimedia.wm.wm_dewiktionary import dewiktionary_de_word_bymeta;
from txcrunch.wikimedia.wm.wm_dewiktionary import dewiktionary_en_word_bymeta;
from txcrunch.wikimedia.wm.wm_dewiktionary import dewiktionary_de_word_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_de_noun import de_noun_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_de_noun import de_noun_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_de_verb import de_verb_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_de_verb import de_verb_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_de_adj import de_adj_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_de_adj import de_adj_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_de_misc import de_misc_bymeta;



def main():


  WIKI_DIR = "/dta/wikimedia";
  OUTPUT_DIR = "/dta/txcrunch";


  if not isfile( OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      dewiktionary_de_word_bymeta( OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv" );
    except:
      try:
        remove( OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/dewiktionary_en_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      dewiktionary_en_word_bymeta( OUTPUT_DIR+"/dewiktionary_en_word_bymeta.csv" );
    except:
      try:
        remove( OUTPUT_DIR+"/dewiktionary_en_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/dewiktionary_de_noun_table.csv" ):

    try:

      dewiktionary_de_word_bycontent(
          WIKI_DIR+"/dewiktionary-20151102-pages-meta-current.xml.bz2",
          OUTPUT_DIR
        );

    except:
      try:
        remove( OUTPUT_DIR+"/dewiktionary_de_noun_table.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/de_noun.csv" ):

    try:

      de_noun_bymeta(
          OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv",
          OUTPUT_DIR+"/de_noun.csv"
        );

      de_noun_bycontent(
          OUTPUT_DIR+"/dewiktionary_de_noun_table.csv",
          OUTPUT_DIR+"/de_noun.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/de_noun.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/de_verb.csv" ):

    try:

      de_verb_bymeta(
          OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv",
          OUTPUT_DIR+"/de_verb.csv"
        );

      de_verb_bycontent(
          OUTPUT_DIR+"/dewiktionary_de_verb_table.csv",
          OUTPUT_DIR+"/de_verb.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/de_verb.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/de_adj.csv" ):

    try:

      de_adj_bymeta(
          OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv",
          OUTPUT_DIR+"/de_adj.csv"
        );

      de_adj_bycontent(
          OUTPUT_DIR+"/dewiktionary_de_adj_table.csv",
          OUTPUT_DIR+"/de_adj.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/de_adj.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/de_misc.csv" ):

    try:

      de_misc_bymeta(
          OUTPUT_DIR+"/dewiktionary_de_word_bymeta.csv",
          OUTPUT_DIR+"/de_misc.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/de_misc.csv" );
      except:
        pass;
      raise;



if __name__ == "__main__":

  import sys;
  main();
