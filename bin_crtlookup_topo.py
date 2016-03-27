from pprint import pprint;

from json import loads as json_loads;
from io import BytesIO;

from os import remove;

from kyotocabinet import DB as kDB;
from umsgpack import unpack as umsgpack_unpack;
from umsgpack import InsufficientDataException;
from umsgpack import packb as umsgpack_packb;

from tclex.geonames.gn.gn import WHITELIST;
from tclex.geonames.gn.gn import BLACKLIST;

from tclex.geonames.gn.gn_normalize_geo import normalize_geo;
from tclex.geonames.gn.unicodedata2 import script;



def crtlookup_topo( output_dir ):


  lookup_dict = kDB();
  lookup_topo = kDB();
  rlookup_topo = kDB();
  info_topo = kDB();

  try:

    lookup_dict.open( output_dir+"/lookup_dict.kch", kDB.OREADER );
    lookup_topo.open( output_dir+"/lookup_topo.kch", kDB.OWRITER | kDB.OCREATE );
    rlookup_topo.open( output_dir+"/rlookup_topo.kch", kDB.OWRITER | kDB.OCREATE );
    info_topo.open( output_dir+"/info_topo.kch", kDB.OWRITER | kDB.OCREATE );


    lookup_topo_ = {};

    with open( output_dir+"/gn_lexicon/xx_toponym.json", "rt" ) as f:

      for line in f:

        row = json_loads( line );

        info_topo.append(
            row[ "_id" ].encode( "utf-8" ),
            umsgpack_packb( row )
          );

        for geoname in row.get( "all_names", [] ):

          geoname_ = normalize_geo( geoname );
          geonames = set([ geoname_ ]);
          if ' / ' in geoname_:
            geonames.add( geoname_.split(' / ')[0] )

          for toponym in geonames:

            if toponym in WHITELIST:

              # print( "[enforcing_whitelisted]", toponym );                
              pass;

            else:

              if toponym in BLACKLIST:
                # print( "[skipping_blacklisted]", toponym );                
                continue;

              if len(toponym) <= 3:
                # print( "[skipping_short]", toponym );
                continue;

              contains_nonlatin = False;
              for ch in toponym:
                chs = script(ch);
                if chs not in [ 'Common', 'Latin', 'Unknown' ]:
                  contains_nonlatin = True;
                  break;
              
              if contains_nonlatin:              
                # print( "[skipping_nonlatin]", toponym );
                continue;

              lexitems = lookup_dict.get( toponym.encode( 'utf-8' ) );

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

                  if lexitem["pos"] in [ "v", "a", "r" ]:
                    pos.add( lexitem["pos"] );

              if pos:
                # print( "[skipping_dictbased]", toponym );
                continue;

            lookup_topo_[ toponym ] \
              =   lookup_topo_.get( toponym, [] ) \
                + [ ( row[ "population" ] or 0,
                      row[ "_id" ] ) ];

            rlookup_topo.append(
                row[ "_id" ].encode( "utf-8" ),
                umsgpack_packb( toponym )
              );

    for ( toponym, pop_id ) in lookup_topo_.items():

      pop_id.sort( reverse=True );

      if not pop_id:
        continue;

      ( pop, geoid ) = pop_id[ 0 ];

      if not pop:

        lookup_topo.append(
            toponym.encode( "utf-8" ),
            umsgpack_packb( None )
          );

      seen = set();

      for ( pop, geoid ) in pop_id:
        
        if geoid in seen:
          continue;
        seen.add( geoid );

        lookup_topo.append(
            toponym.encode( "utf-8" ),
            umsgpack_packb( geoid )
          );

  except:

    try:
      
      info_topo.close();
      rlookup_topo.close();
      lookup_topo.close();
      lookup_dict.close();

      remove( output_dir+"/info_topo.kch" );
      remove( output_dir+"/rlookup_topo.kch" );
      remove( output_dir+"/lookup_topo.kch" );

      info_topo = None;
      rlookup_topo = None;
      lookup_topo = None;
      lookup_dict = None; 

    except:
      pass;

    raise;

  finally:

    if info_topo is not None:
      info_topo.close();

    if rlookup_topo is not None:
      rlookup_topo.close();

    if lookup_topo is not None:
      lookup_topo.close();

    if lookup_dict is not None:
      lookup_dict.close();



def main( output_dir ):

  crtlookup_topo( output_dir );



if __name__ == "__main__":

  import sys;
  main();
