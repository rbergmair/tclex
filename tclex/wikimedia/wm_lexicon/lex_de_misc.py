__all__ \
  = [ "de_misc_bymeta" ];


from txcrunch.wikimedia.wm.mw_cleanup import mw_cleanup;



def de_misc_bymeta( dewiktionary_de_word_bymeta_fn, out_fn ):

  w = 0;

  with open( dewiktionary_de_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );

        if pos != 'x':
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
              ( "|"\
                 .join(
                      [ L[0],
                        L[0].upper(),
                        L[0].upper(),
                        '1',
                        '' ]
                    ) ) \
            + '\n'
          );

  return w;
