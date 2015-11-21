__all__ \
  = [ "mw_funky",
      "mw_dewikify",
      "mw_unescape",
      "mw_cleanup" ]


from html.parser import HTMLParser;
from string import ascii_letters, digits;



def mw_funky( s ):
  
  if not s:
    return True;
  
  if "&" in s:
    return True;

  if "#" in s:
    return True;

  if ";" in s:
    return True;
  
  s2 = s.encode( "ascii", errors="xmlcharrefreplace" ).decode( "ascii" );
  
  s1 = "";
  for ch in s2:
    if ch == " " or ch in ( ascii_letters + digits + "&;#-.'" ):
      s1 += ch;

  return ( s1 != s2 );



def mw_dewikify( s ):
  
  s = s.replace( "'''", "" );
  s = s.replace( ">", " " );
  return s;



def mw_unescape( r ):

  p = HTMLParser();
  
  blowout = 0;
  
  while "&amp;" in r:
    r = r.replace( "&nbsp;", " " );
    r = p.unescape( r );
    blowout += 1;
    if blowout > 100:
      break;

  r = r.replace( "&nbsp;", " " );
  r = p.unescape( r );
  
  return r.strip();



def mw_cleanup( r, discardable_prefixes=None ):
  
  r = mw_unescape( r );
  r = mw_dewikify( r );

  r = r.replace( "\t", " " );
  
  r = r.strip();
  
  def splitquote( x ):
    
    done_split = False; 
    
    if x.startswith( "''" ) and x.endswith( "''" ):
      x = r[2:-2];
    
    x = x.replace( "(''", "''(" );
    x = x.replace( "'')", ")''" );    
  
    a = x.find( "''" );
    if a != -1:
      a_ = x[ a+2: ]
      b = a_.find( "''" );
      if b != -1:
        
        left = x[ :a ];
        right = x[ a+2+b+2: ];
        quoted = x[ a+2:a+2+b ];

        if    quoted == "or" \
           or quoted.startswith( "or " ) \
           or quoted.find(":") != -1 \
           or ( quoted.startswith( "(" ) and quoted.endswith( ")" ) ):
        
          print( "subsplit ", x, " -> ", left, " / ", right );

          for v in splitquote( left ):
            yield mw_unescape(v).strip();
            done_split = True; 
          for v in splitquote( right ):
            yield mw_unescape(v).strip();
            done_split = True;
        
        else:
          
          print( "WARNING! funky: " + repr(x) )
          yield "";
    
    if not done_split:
      yield mw_unescape(x).strip();

  for r_ in splitquote( r ):
    
    if r_.find( "''" ) != -1:
      print( "WARNING! funky: " + repr(r) );
      continue;
    
    for s in r_.split( ";" ):
      for t in s.split( "/" ):
        for u_ in t.split( "," ):
          for u in u_.split( " or " ):
            
            u = u.strip();
            if not u:
              continue;
            
            ux = u.find( " " );
            if ux != -1:
              uy = u[ :ux ];
              if uy == "or":
                continue;
          
            u = u.strip();
      
            if len(u) < 3:
              continue;
            
            if discardable_prefixes is not None:
              
              u_ = u.find( " " );
              if u_ != -1:
                
                pref = u[ :u_ ];
                pref = pref.replace( "(", "" );
                pref = pref.replace( ")", "" );
                pref = pref.upper();
                
                if pref in discardable_prefixes:
                  u = u[ u_+1: ].strip();
            
            if u[0] == "(" and u[-1] == ")":
              u = u[1:-1];
            elif u[0] == "(" and u.find(")") == -1:
              u = u[1:];
            elif u[-1] == ")" and u.find("(") == -1:
              u = u[:-1];
            
            u0 = u.find( "(");
            u1 = u.find( ")" );
            
            if u0 == -1 and u1 == -1:
    
              if mw_funky( u ):
                print( "WARNING! funky " + repr(u) );
              else:
                yield mw_unescape(u).strip();
            
            elif u0 != -1 and u1 != -1 and u1 > u0:
            
              v0 = u[:u0] + u[u1+1:];
              v1 = u.replace( "(", "" ).replace( ")", "" );
              
              print( "expanded ", repr(u), " -> ", repr(v0), ",", repr(v1) );
            
              if mw_funky( v0 ):
                print( "WARNING! funky " + repr(v0) );
              else:
                yield mw_unescape(v0).strip();
    
              if mw_funky( v1 ):
                print( "WARNING! funky " + repr(v1) );
              else:
                yield mw_unescape(v1).strip();
            
            else:
              
              print( "WARNING! funky " + repr(u) );
              pass;
