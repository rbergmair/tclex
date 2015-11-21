__all__ \
  = [ "en_noun_bymeta",
      "en_noun_bycontent" ]


from tclex.wikimedia.wm.mw_cleanup import mw_cleanup;



def en_noun_bymeta( enwiktionary_en_word_bymeta_fn, out_fn ):

  w = 0;

  with open( enwiktionary_en_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );

        if pos != 'n':
          continue;

        catid = int( catid );

        if catid == 53124:
          continue;

        L = list( mw_cleanup( lemma ) );
        if len(L) == 0:
          print( "WARNING! funky lemma" );
          w += 1;
          continue;
        elif len(L) > 1:
          print( "WARNING! funky lemma " + repr(L) );
          w += 1;
          continue;

        outf.write(
            '|'.join( [ L[0], L[0].upper(), L[0].upper(), "1", "" ] ) + '\n'
          );

  return w;



def en_noun_bycontent( enwiktionary_en_noun_fn, out_fn ):

  w = 0;

  with open( enwiktionary_en_noun_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        line = line.split( '|' );
        line = [ line[0], line[3], line[4] ];

        L = list( mw_cleanup( line[0] ) );

        if len(L) == 0:
          print( "WARNING! funky lemma" );
          w += 1;
          continue;
        elif len(L) > 1:
          print( "WARNING! funky lemma " + repr(L) );
          w += 1;
          continue;
        
        j = 0;
        
        for i in range(1,3):
          
          r = line[i];
          r = r.replace( "+", "" );
          r = r.replace( "[[", "" );
          r = r.replace( "]]", "" );

          for u in mw_cleanup( r ):
            
            j += 1;
            outf.write(
                "|"\
                 .join(
                      [ u,
                        u.upper(),
                        L[0].upper(),
                        str(j),
                        ( "", "singular", "plural" )[ i ] ]
                    ) \
                + "\n"
              );

  return w;
