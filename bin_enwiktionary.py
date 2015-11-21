from os.path import isfile;
from os import remove;

from txcrunch.wikimedia.wm.wm_enwiktionary import enwiktionary_de_word_bymeta;
from txcrunch.wikimedia.wm.wm_enwiktionary import enwiktionary_en_word_bymeta;
from txcrunch.wikimedia.wm.wm_enwiktionary import enwiktionary_en_word_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_en_noun import en_noun_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_en_noun import en_noun_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_en_verb import en_verb_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_en_verb import en_verb_regular_bycontent;
from txcrunch.wikimedia.wm_lexicon.lex_en_verb import en_verb_irregular_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_en_adj import en_adj_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_en_adj import en_adj_irregular_bycontent;
from txcrunch.wikimedia.wm_lexicon.lex_en_adj import en_adj_regular_bycontent;

from txcrunch.wikimedia.wm_lexicon.lex_en_adv import en_adv_bymeta;
from txcrunch.wikimedia.wm_lexicon.lex_en_adv import en_adv_irregular_bycontent;
from txcrunch.wikimedia.wm_lexicon.lex_en_adv import en_adv_regular_bycontent;



def main():


  WIKI_DIR = "/dta/wikimedia";
  OUTPUT_DIR = "/dta/txcrunch";


  if not isfile( OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      enwiktionary_en_word_bymeta( OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv" );
    except:
      try:
        remove( OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/enwiktionary_de_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      enwiktionary_de_word_bymeta( OUTPUT_DIR+"/enwiktionary_de_word_bymeta.csv" );
    except:
      try:
        remove( OUTPUT_DIR+"/enwiktionary_de_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/enwiktionary_en_noun.csv" ):

    try:

      enwiktionary_en_word_bycontent(
          WIKI_DIR+"/enwiktionary-20151102-pages-meta-current.xml.bz2",
          OUTPUT_DIR
        );

    except:
      try:
        remove( OUTPUT_DIR+"/enwiktionary_en_noun.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/en_noun.csv" ):

    try:

      en_noun_bymeta(
          OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv",
          OUTPUT_DIR+"/en_noun.csv"
        );

      en_noun_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_noun.csv",
          OUTPUT_DIR+"/en_noun.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/en_noun.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/en_verb.csv" ):

    try:

      en_verb_bymeta(
          OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv",
          OUTPUT_DIR+"/en_verb.csv"
        );

      en_verb_regular_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_verb_regular.csv",
          OUTPUT_DIR+"/en_verb.csv"
        );

      en_verb_irregular_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_verb_irregular.csv",
          OUTPUT_DIR+"/en_verb.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/en_verb.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/en_adj.csv" ):

    try:

      en_adj_bymeta(
          OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv",
          OUTPUT_DIR+"/en_adj.csv"
        );

      en_adj_irregular_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_adj_irregular.csv",
          OUTPUT_DIR+"/en_adj.csv"
        );

      en_adj_regular_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_adj_regular.csv",
          OUTPUT_DIR+"/en_adj.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/en_adj.csv" );
      except:
        pass;
      raise;


  if not isfile( OUTPUT_DIR+"/en_adv.csv" ):

    try:

      en_adv_bymeta(
          OUTPUT_DIR+"/enwiktionary_en_word_bymeta.csv",
          OUTPUT_DIR+"/en_adv.csv"
        );

      en_adv_irregular_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_adv_irregular.csv",
          OUTPUT_DIR+"/en_adv.csv"
        );

      en_adv_regular_bycontent(
          OUTPUT_DIR+"/enwiktionary_en_adv_regular.csv",
          OUTPUT_DIR+"/en_adv.csv"
        );

    except:
      try:
        remove( OUTPUT_DIR+"/en_adv.csv" );
      except:
        pass;
      raise;



if __name__ == "__main__":

  import sys;
  main();
