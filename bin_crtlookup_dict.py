from os.path import isdir;
from os import remove;

from kyotocabinet import DB as kDB;
from umsgpack import packb;



def add_from_csv( lookup_dict, rlookup_dict, in_fn, lg, pos ):

  with open( in_fn, "rt" ) as f:

    for line in f:

      if line and line[-1] == '\n':
        line = line[:-1];

      line = line.split( '|' );

      ( form, form_lookup, lemma, id_, gtag ) = line;

      lookup_dict.append(
          form_lookup.encode( 'utf-8' ),
          packb(
              { "form": form,
                "lemma": lemma,
                "id": id_,
                "gtag": gtag,
                "lg": lg,
                "pos": pos }
            )
        );

      rlookup_dict.append(
          lemma.encode( 'utf-8' ),
          packb(
              { "form": form,
                "lemma": lemma,
                "id": id_,
                "gtag": gtag,
                "lg": lg,
                "pos": pos }
            )
        );



def crtlookup_dict( output_dir ):

  assert isdir( output_dir );

  inmap \
    = [ ( "en_noun.csv", "en", "n" ),
        ( "en_verb.csv", "en", "v" ),
        ( "en_adj.csv", "en", "a" ),
        ( "en_adv.csv", "en", "r" ),
        ( "de_noun.csv", "de", "n" ),
        ( "de_verb.csv", "de", "v" ),
        ( "de_adj.csv", "de", "a" ),
        ( "de_misc.csv", "de", "x" ) ];

  lookup_dict = kDB();
  rlookup_dict = kDB();

  try:

    lookup_dict.open(
        output_dir + "/lookup_dict.kch",
        kDB.OWRITER | kDB.OCREATE
      );

    rlookup_dict.open(
        output_dir + "/rlookup_dict.kch",
        kDB.OWRITER | kDB.OCREATE
      );

    for ( fn, lang, pos ) in inmap:
      add_from_csv(
          lookup_dict,
          rlookup_dict,
          output_dir+"/wm_lexicon/"+fn,
          lang,
          pos
        );

  except:

    try:
      lookup_dict.close();
      rlookup_dict.close();
      remove( output_dir+"/lookup_dict.kch" );
      remove( output_dir+"/rlookup_dict.kch" );
      lookup_dict = None;
      rlookup_dict = None;
    except:
      pass;

    raise;

  finally:

    if lookup_dict is not None:
      lookup_dict.close();
    if rlookup_dict is not None:
      rlookup_dict.close();



def main( output_dir ):

  crtlookup_dict( output_dir );



if __name__ == "__main__":

  import sys;
  main();
