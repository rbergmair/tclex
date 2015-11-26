from os.path import isfile;
from os import remove;
from os import makedirs;

from tclex.geonames.gn_lexicon.lex_xx_toponym import xx_toponym;



def import_geonames( output_dir, gn_dir ):

  makedirs( output_dir+"/gn_lexicon", exist_ok=True );

  if not isfile( output_dir+"/gn_lexicon/xx_toponym.json" ):

    try:

      xx_toponym(
          gn_dir,
          "AT.txt.bz2",
          output_dir+"/gn_lexicon/xx_toponym.json"
        );

      xx_toponym(
          gn_dir,
          "DE.txt.bz2",
          output_dir+"/gn_lexicon/xx_toponym.json"
        );

      xx_toponym(
          gn_dir,
          "CH.txt.bz2",
          output_dir+"/gn_lexicon/xx_toponym.json"
        );

    except:
      try:
        remove( output_dir+"/gn_lexicon/xx_toponym.json" );
      except:
        pass;
      raise;



def main( output_dir, from_, gn_dir ):

  assert from_ == "from";
  import_geonames( output_dir, gn_dir );



if __name__ == "__main__":

  import sys;
  main();
