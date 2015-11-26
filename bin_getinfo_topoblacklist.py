from pprint import pprint;

from json import loads as json_loads;
from io import BytesIO;

from kyotocabinet import DB as kDB;
from umsgpack import unpack as umsgpack_unpack;
from umsgpack import InsufficientDataException;

from tclex.geonames.gn.gn_normalize_geo import normalize_geo;
from tclex.geonames.gn.unicodedata2 import script;



def getinfo_topoblacklist( output_dir ):


  black_short = [];
  white_short = [];
  black_by_pop = [];
  white_by_pop = [];


  kdb = kDB();

  try:

    kdb.open( output_dir+"/lookup_dict.kch", kDB.OREADER );


    maxpop_by_toponym = {};

    with open( output_dir+"/gn_lexicon/xx_toponym.json", "rt" ) as f:

      for line in f:

        row = json_loads( line );

        for geoname in row.get( "all_names", [] ):

          geoname_ = normalize_geo( geoname );
          geonames = set([ geoname_ ]);
          if ' / ' in geoname_:
            geonames.add( geoname_.split(' / ')[0] )

          for geoname_ in geonames:

            contains_nonlatin = False;
            for ch in geoname_:
              chs = script(ch);
              if chs not in [ 'Common', 'Latin', 'Unknown' ]:
                contains_nonlatin = True;
                break;
            
            if contains_nonlatin:
              continue;

            if not geoname_ in maxpop_by_toponym:
              maxpop_by_toponym[ geoname_ ] = row.get( "population" ) or 0;
            else:
              maxpop_by_toponym[ geoname_ ] \
                = max(
                      maxpop_by_toponym[ geoname_ ],
                      row.get( "population" ) or 0
                    );


    for ( toponym, maxpop ) in maxpop_by_toponym.items():

      lexitems = kdb.get( toponym.encode( 'utf-8' ) );

      pos = set();      

      if lexitems is not None:

        lexitems_ = BytesIO( lexitems );

        while True:

          try:
            lexitem = umsgpack_unpack( lexitems_ );
          except InsufficientDataException: 
            lexitem = None;

          if lexitem is None:
            break;

          pos.add( lexitem["pos"] );

      if "x" in pos and "n" in pos:
        pos.remove( "n" );
      if "x" in pos:
        pos.remove( "x" );

      if pos:

        if len( toponym ) < 3:
          black_short.append( toponym );

        black_by_pop.append( ( maxpop, toponym ) );
        black_by_pop.sort( reverse=True );
        if len( black_by_pop ) > 700:
          black_by_pop = black_by_pop[:700];

      else:

        if len( toponym ) <= 3:
          white_short.append( toponym );

        white_by_pop.append( ( maxpop, toponym ) );
        white_by_pop.sort( reverse=True );
        if len( white_by_pop ) > 700:
          white_by_pop = white_by_pop[:700];


  finally:

    kdb.close();


  print( "black_short" );
  pprint( black_short );

  print( "white_short" );
  pprint( white_short );

  print( "black_by_pop" );
  # pprint([ x for (pop,x) in black_by_pop ]);
  pprint( black_by_pop );

  print( "white_by_pop" );
  # pprint([ x for (pop,x) in white_by_pop ]);
  pprint( white_by_pop );



def main( output_dir ):

  getinfo_topoblacklist( output_dir );



if __name__ == "__main__":

  import sys;
  main();
