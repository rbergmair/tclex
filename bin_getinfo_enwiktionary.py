from os.path import isfile;
from os import remove;
from pprint import pprint;

from tclex.wikimedia.wm.mw import MediawikiMetadataTreewalker;


def print_categories( root ):

  conn_args = [ "127.0.0.1", "enwiktionary", "root", "" ];

  with MediawikiMetadataTreewalker( *conn_args ) as tree:

    pprint(
        tree.page_title_by_id(
            tree.subcat_pageids_trans_closure( root )
          )
      );


def getinfo_enwiktionary():

  print_categories( "English_verbs" );
  print_categories( "English_nouns" );
  print_categories( "English_adjectives" );
  print_categories( "English_adverbs" );


def main():

  getinfo_enwiktionary(): 


if __name__ == "__main__":

  import sys;
  main();
