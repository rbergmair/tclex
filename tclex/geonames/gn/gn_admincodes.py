from bz2 import open as bz2_open;



def load_admincodes( gn_dir ):

  rslt = {};

  with bz2_open( gn_dir + "/admin2Codes.txt.bz2", "rt", encoding="utf-8" ) as f:

    for line in f:    
      
      if line[-1] == "\n":
        line = line[:-1];
      
      line = line.split( "\t" );
      
      rslt[ line[0] ] = int(line[3]);

  with bz2_open( gn_dir + "/admin1CodesASCII.txt.bz2", "rt", encoding="utf-8" ) as f:
    
    for line in f:
      
      if line[-1] == "\n":
        line = line[:-1];
      
      line = line.split( "\t" );
      
      rslt[ line[0] ] = int(line[3]);  

  return rslt;
