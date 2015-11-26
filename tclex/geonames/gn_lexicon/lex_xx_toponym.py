from bz2 import open as bz2_open;
from pprint import pprint;
from json import dump as json_dump;


from tclex.geonames.gn.gn import MNEMONICs;
from tclex.geonames.gn.gn_admincodes import load_admincodes;
from tclex.geonames.gn.gn_hierarchy import load_hierarchy;
from tclex.geonames.gn.gn_hierarchy import compute_hierarchy_tc;



def xx_toponym( gn_dir, in_fn, out_fn ):

  rootid = None;

  if in_fn == "AT.txt.bz2":
    rootid = 2782113;
    assert MNEMONICs[ rootid ] == "AT";
  elif in_fn == "DE.txt.bz2":
    rootid = 2921044;
    assert MNEMONICs[ rootid ] == "DE";
  elif in_fn == "CH.txt.bz2":
    rootid = 2658434;
    assert MNEMONICs[ rootid ] == "CH";
  else:
    assert False;

  admincodes = load_admincodes( gn_dir );
  hierarchy = load_hierarchy( gn_dir );

  with open( out_fn, "at" ) as outf:
    
    with bz2_open( gn_dir + '/' + in_fn, "rt", encoding="utf-8" ) as f:
      
      for line in f:
        
        if line[-1] == "\n":
          line = line[:-1];
        
        ( geonameid,
          name,
          asciiname,
          alternatenames,
          latitude,
          longitude,
          feature_class,
          feature_code,
          country_code,
          cc2,
          admin1_code,
          admin2_code,
          admin3_code,
          admin4_code,
          population,
          elevation,
          dem,
          timezone,
          modification_date ) = line.split( "\t" );
        
        if feature_class not in [ "A", "P" ]:
          continue;
        
        try:
          
          if latitude:
            latitude = float(latitude);
          else:
            latitude = None;
          
          if longitude:
            longitude = float(longitude);
          else:
            longitude = None;
          
          if elevation:
            elevation = float(elevation);
          else:
            elevation = None;
          
          if population:
            population = int(population);
          else:
            population = None;
          
          if population == 0:
            population = None;
          
          if dem:
            dem = int(dem);
          else:
            dem = None;
          
          geonameid = int(geonameid);
        
        except:
          
          print( line );
          raise;
        
        admincode = "";
        admincode += country_code;
        if admin1_code:
          admincode += "." + admin1_code;
          if admin2_code:
            admincode += "." + admin2_code;
        if not admincode in admincodes:
          admincode_geonameid=rootid;
        else:  
          admincode_geonameid = admincodes[ admincode ];
        
        admincode_geonameid = int(admincode_geonameid);

        ( mnem, admin_nodeid, admin_parents ) = \
            compute_hierarchy_tc( admincode_geonameid, rootid, hierarchy );

        if admincode_geonameid != geonameid:
          
          parents = set([admin_nodeid]) | admin_parents;
          
          if mnem is not None:
            geonameid_ = mnem + "_" + hex(geonameid)[2:].zfill(6);
          else:
            geonameid_ = hex(geonameid)[2:].zfill(6);
        
        else:
          
          parents = admin_parents;
          geonameid_ = admin_nodeid;
        
        name=name.strip();
        asciiname = asciiname.strip();
        
        all_names = [];
        if name:
          all_names.append( name );
        
        if asciiname:
          all_names.append( asciiname );
        for alternate in alternatenames.split(","):
          alternate = alternate.strip();
          if alternate:
            all_names.append( alternate );

        row \
          = { "_id": geonameid_,
              "geonameid": geonameid,
              "name": name,
              "asciiname": asciiname,
              "all_names": list( sorted( all_names ) ),
              "latitude": latitude,
              "longitude": longitude,
              "feature_class": feature_class,
              "feature_code": feature_code,
              "country_code": country_code,
              "cc2": cc2,
              "population": population,
              "elevation": elevation,
              "dem": dem,
              "timezone": timezone,
              "modification_date": modification_date,
              "parents": list( sorted( parents ) ) };

        json_dump( row, outf );
        outf.write( '\n' );
