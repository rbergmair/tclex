from os.path import isfile;
from os import remove;
from os import makedirs;

from tclex.wikimedia.wm.wm_enwiktionary import enwiktionary_de_word_bymeta;
from tclex.wikimedia.wm.wm_enwiktionary import enwiktionary_en_word_bymeta;
from tclex.wikimedia.wm.wm_enwiktionary import enwiktionary_en_word_bycontent;

from tclex.wikimedia.wm_lexicon.lex_en_noun import en_noun_bymeta;
from tclex.wikimedia.wm_lexicon.lex_en_noun import en_noun_bycontent;

from tclex.wikimedia.wm_lexicon.lex_en_verb import en_verb_bymeta;
from tclex.wikimedia.wm_lexicon.lex_en_verb import en_verb_regular_bycontent;
from tclex.wikimedia.wm_lexicon.lex_en_verb import en_verb_irregular_bycontent;

from tclex.wikimedia.wm_lexicon.lex_en_adj import en_adj_bymeta;
from tclex.wikimedia.wm_lexicon.lex_en_adj import en_adj_irregular_bycontent;
from tclex.wikimedia.wm_lexicon.lex_en_adj import en_adj_regular_bycontent;

from tclex.wikimedia.wm_lexicon.lex_en_adv import en_adv_bymeta;
from tclex.wikimedia.wm_lexicon.lex_en_adv import en_adv_irregular_bycontent;
from tclex.wikimedia.wm_lexicon.lex_en_adv import en_adv_regular_bycontent;



def main( wiki_dir, output_dir ):


  makedirs( output_dir+"/wm", exist_ok=True );
  makedirs( output_dir+"/wm_lexicon", exist_ok=True );


  if not isfile( output_dir+"/wm/enwiktionary_en_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      enwiktionary_en_word_bymeta( output_dir+"/wm/enwiktionary_en_word_bymeta.csv" );
    except:
      try:
        remove( output_dir+"/wm/enwiktionary_en_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm/enwiktionary_de_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      enwiktionary_de_word_bymeta( output_dir+"/wm/enwiktionary_de_word_bymeta.csv" );
    except:
      try:
        remove( output_dir+"/wm/enwiktionary_de_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm/enwiktionary_en_noun.csv" ):

    try:

      enwiktionary_en_word_bycontent(
          wiki_dir+"/enwiktionary-20151102-pages-meta-current.xml.bz2",
          output_dir+"/wm"
        );

    except:
      try:
        remove( output_dir+"/wm/enwiktionary_en_noun.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/en_noun.csv" ):

    try:

      en_noun_bymeta(
          output_dir+"/wm/enwiktionary_en_word_bymeta.csv",
          output_dir+"/wm_lexicon/en_noun.csv"
        );

      en_noun_bycontent(
          output_dir+"/wm/enwiktionary_en_noun.csv",
          output_dir+"/wm_lexicon/en_noun.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/en_noun.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/en_verb.csv" ):

    try:

      en_verb_bymeta(
          output_dir+"/wm/enwiktionary_en_word_bymeta.csv",
          output_dir+"/wm_lexicon/en_verb.csv"
        );

      en_verb_regular_bycontent(
          output_dir+"/wm/enwiktionary_en_verb_regular.csv",
          output_dir+"/wm_lexicon/en_verb.csv"
        );

      en_verb_irregular_bycontent(
          output_dir+"/wm/enwiktionary_en_verb_irregular.csv",
          output_dir+"/wm_lexicon/en_verb.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/en_verb.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/en_adj.csv" ):

    try:

      en_adj_bymeta(
          output_dir+"/wm/enwiktionary_en_word_bymeta.csv",
          output_dir+"/wm_lexicon/en_adj.csv"
        );

      en_adj_irregular_bycontent(
          output_dir+"/wm/enwiktionary_en_adj_irregular.csv",
          output_dir+"/wm_lexicon/en_adj.csv"
        );

      en_adj_regular_bycontent(
          output_dir+"/wm/enwiktionary_en_adj_regular.csv",
          output_dir+"/wm_lexicon/en_adj.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/en_adj.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/en_adv.csv" ):

    try:

      en_adv_bymeta(
          output_dir+"/wm/enwiktionary_en_word_bymeta.csv",
          output_dir+"/wm_lexicon/en_adv.csv"
        );

      en_adv_irregular_bycontent(
          output_dir+"/wm/enwiktionary_en_adv_irregular.csv",
          output_dir+"/wm_lexicon/en_adv.csv"
        );

      en_adv_regular_bycontent(
          output_dir+"/wm/enwiktionary_en_adv_regular.csv",
          output_dir+"/wm_lexicon/en_adv.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/en_adv.csv" );
      except:
        pass;
      raise;



if __name__ == "__main__":

  import sys;
  main();
