from bz2 import open as bz2_open;


from tclex.geonames.gn.gn import MNEMONICs;



def load_hierarchy( gn_dir ):

  rslt = {};

  with bz2_open( gn_dir + "/hierarchy.txt.bz2", "rt", encoding="utf-8" ) as f:

    for line in f:    
      
      if line[-1] == "\n":
        line = line[:-1];
      
      line = line.split( "\t" );
      
      line0 = int( line[0] );
      line1 = int( line[1] );
      
      if not line1 in rslt:
        rslt[ line1 ] = [];
      rslt[ line1 ].append( line0 );

  return rslt;



def compute_hierarchy_tc( nodeid, rootid, hierarchy, hierarchy_tc=None ):

  if hierarchy_tc is None:
    hierarchy_tc = {};

  if nodeid in hierarchy_tc:
    return hierarchy_tc[ nodeid ];
  
  mnem = None;
  nodeid_ = None;
  if nodeid in MNEMONICs:
    mnem = MNEMONICs[nodeid];
    nodeid_ = mnem;
  
  if ( not nodeid in hierarchy ) or ( nodeid == rootid ):
    hierarchy_tc[ nodeid ] \
      = ( mnem, nodeid_ or hex(nodeid)[2:].zfill(6), set() );
    return hierarchy_tc[ nodeid ];
  
  parents = [];
  pmnems = set();
  
  for pnodeid in hierarchy[nodeid]:
  
    ( pmnem, pnodeid_, pparents ) \
        = compute_hierarchy_tc( pnodeid, rootid, hierarchy, hierarchy_tc );
    
    parents.append( ( pmnem, pnodeid_, pparents ) );
    pmnems.add( pmnem );
  
  pmnem1 = None;
  pmnem2 = None;
  pmnem3 = None;
  
  if not None in pmnems:
    
    for m in pmnems:
      
      m_ = m.split("_");
      assert 1 <= len(m_) <= 3;

      pmnem1_ = m_[0] if len(m_) >= 1 else "?";
      pmnem2_ = m_[0] + "_" + m_[1] if len(m_) >= 2 else "?";
      pmnem3_ = m_[0] + "_" + m_[1] + "_" + m_[2] if len(m_) >= 3 else "?";
      
      if pmnem1 is None:
        pmnem1 = pmnem1_;
      if pmnem1 != pmnem1_:
        pmnem1 = "#";
      
      if pmnem2 is None:
        pmnem2 = pmnem2_;
      if pmnem2 != pmnem2_:
        pmnem2 = "#";
      
      if pmnem3 is None:
        pmnem3 = pmnem3_;
      if pmnem3 != pmnem3_:
        pmnem3 = "#";
  
  if pmnem3 is not None and pmnem3 != "?" and pmnem3 != "#":
    assert pmnem2 is not None and pmnem2 != "?" and pmnem2 != "#";
    pmnem = pmnem3;
  elif pmnem2 is not None and pmnem2 != "?" and pmnem2 != "#":
    assert pmnem1 is not None and pmnem1 != "?" and pmnem1 != "#";
    pmnem = pmnem2;
  elif pmnem1 is not None and pmnem1 != "?" and pmnem1 != "#":
    pmnem = pmnem1;
  else:
    pmnem = None;
  
  parents_ = set();
  for ( pmnem_, pnodeid_, pparents ) in parents:
    parents_.add( pnodeid_ );
    parents_ |= pparents;
  
  if mnem is None:
    assert nodeid_ is None;
    mnem = pmnem;
    if mnem is not None:
      nodeid_ = mnem + "_" + hex(nodeid)[2:].zfill(6);
  
  hierarchy_tc[ nodeid ] \
    = ( mnem, nodeid_ or hex(nodeid)[2:].zfill(6), parents_ );
  
  return hierarchy_tc[ nodeid ];
