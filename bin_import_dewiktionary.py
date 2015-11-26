from os.path import isfile;
from os import remove;
from os import makedirs;

from tclex.wikimedia.wm.wm_dewiktionary import dewiktionary_de_word_bymeta;
from tclex.wikimedia.wm.wm_dewiktionary import dewiktionary_en_word_bymeta;
from tclex.wikimedia.wm.wm_dewiktionary import dewiktionary_de_word_bycontent;

from tclex.wikimedia.wm_lexicon.lex_de_noun import de_noun_bymeta;
from tclex.wikimedia.wm_lexicon.lex_de_noun import de_noun_bycontent;

from tclex.wikimedia.wm_lexicon.lex_de_verb import de_verb_bymeta;
from tclex.wikimedia.wm_lexicon.lex_de_verb import de_verb_bycontent;

from tclex.wikimedia.wm_lexicon.lex_de_adj import de_adj_bymeta;
from tclex.wikimedia.wm_lexicon.lex_de_adj import de_adj_bycontent;

from tclex.wikimedia.wm_lexicon.lex_de_misc import de_misc_bymeta;



def import_dewiktionary( output_dir, wiki_dir ):

  makedirs( output_dir+"/wm", exist_ok=True );
  makedirs( output_dir+"/wm_lexicon", exist_ok=True );


  if not isfile( output_dir+"/wm/dewiktionary_de_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      dewiktionary_de_word_bymeta( output_dir+"/wm/dewiktionary_de_word_bymeta.csv" );
    except:
      try:
        remove( output_dir+"/wm/dewiktionary_de_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm/dewiktionary_en_word_bymeta.csv" ):
    
    try:

      import mysql.connector;

    except ImportError:

      print( "Can't seem to be able to import mysql.connector.");
      print( "Please make sure it's installed and importable." );
      return;

    try:
      dewiktionary_en_word_bymeta( output_dir+"/wm/dewiktionary_en_word_bymeta.csv" );
    except:
      try:
        remove( output_dir+"/wm/dewiktionary_en_word_bymeta.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm/dewiktionary_de_noun_table.csv" ):

    try:

      dewiktionary_de_word_bycontent(
          wiki_dir+"/dewiktionary-20151102-pages-meta-current.xml.bz2",
          output_dir+"/wm"
        );

    except:
      try:
        remove( output_dir+"/wm/dewiktionary_de_noun_table.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/de_noun.csv" ):

    try:

      de_noun_bymeta(
          output_dir+"/wm/dewiktionary_de_word_bymeta.csv",
          output_dir+"/wm_lexicon/de_noun.csv"
        );

      de_noun_bycontent(
          output_dir+"/wm/dewiktionary_de_noun_table.csv",
          output_dir+"/wm_lexicon/de_noun.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/de_noun.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/de_verb.csv" ):

    try:

      de_verb_bymeta(
          output_dir+"/wm/dewiktionary_de_word_bymeta.csv",
          output_dir+"/wm_lexicon/de_verb.csv"
        );

      de_verb_bycontent(
          output_dir+"/wm/dewiktionary_de_verb_table.csv",
          output_dir+"/wm_lexicon/de_verb.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/de_verb.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/de_adj.csv" ):

    try:

      de_adj_bymeta(
          output_dir+"/wm/dewiktionary_de_word_bymeta.csv",
          output_dir+"/wm_lexicon/de_adj.csv"
        );

      de_adj_bycontent(
          output_dir+"/wm/dewiktionary_de_adj_table.csv",
          output_dir+"/wm_lexicon/de_adj.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/de_adj.csv" );
      except:
        pass;
      raise;


  if not isfile( output_dir+"/wm_lexicon/de_misc.csv" ):

    try:

      de_misc_bymeta(
          output_dir+"/wm/dewiktionary_de_word_bymeta.csv",
          output_dir+"/wm_lexicon/de_misc.csv"
        );

    except:
      try:
        remove( output_dir+"/wm_lexicon/de_misc.csv" );
      except:
        pass;
      raise;



def main( output_dir, from_, wiki_dir ):

  assert from_ == "from";
  import_dewiktionary( output_dir, wiki_dir );



if __name__ == "__main__":

  import sys;
  main();
