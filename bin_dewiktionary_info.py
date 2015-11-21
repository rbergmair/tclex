from os.path import isfile;
from os import remove;
from pprint import pprint;

from tclex.wikimedia.wm.mw import MediawikiMetadataTreewalker;


def print_categories( root ):

  conn_args = [ "127.0.0.1", "dewiktionary", "root", "" ];

  with MediawikiMetadataTreewalker( *conn_args ) as tree:

    pprint(
        tree.page_title_by_id(
            tree.subcat_pageids_trans_closure( root )
          )
      );


def main():

  print_categories( "Verb_(Deutsch)" );
  print_categories( "Substantiv_(Deutsch)" );
  print_categories( "Adjektiv_(Deutsch)" );
  print_categories( "Adverb_(Deutsch)" );


if __name__ == "__main__":

  import sys;
  main();
