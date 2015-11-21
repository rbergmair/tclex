__all__ \
  = [ "en_verb_bymeta",
      "en_verb_regular_bycontent",
      "en_verb_irregular_bycontent" ];


from tclex.wikimedia.wm.mw_cleanup import mw_cleanup;
from tclex.wikimedia.wm.mw_cleanup import mw_unescape;



def de_verb_bymeta( dewiktionary_de_word_bymeta_fn, out_fn ):

  cats \
    = { 164226: "",
         57755: "",
         65640: "" };

  w = 0;

  with open( dewiktionary_de_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );

        if pos != 'v':
          continue;

        catid = int( catid );
        
        if not catid in cats:
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
            "|"\
             .join(        
                [ L[0], L[0].upper(), L[0].upper(), "1", cats[catid] ]
              )
            + "\n"
          );

  return w;



def de_verb_bycontent( dewiktionary_de_verb_table_fn, out_fn ):

  flds \
    = [ "lemma",
        "pres1sg", "pres2sg", "pres3sg",
        "praet1sg", "praet3sgn", "part2",
        "conj21sg", "conj23sgn",
        "impsg", "imppl" ];

  w = 0;

  with open( dewiktionary_de_verb_table_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        line = line.split( '|' );

        L = list( mw_cleanup( line[0] ) );

        if len(L) == 0:
          print( "WARNING! funky lemma" );
          w += 1;
          continue;
        elif len(L) > 1:
          print( "WARNING! funky lemma " + repr(L) );
          w += 1;
          continue;

        j = 1;

        outf.write(
            "|"\
             .join(
                  [ L[0],
                    L[0].upper(),
                    L[0].upper(),
                    str(j),
                    "inf" ]
                ) \
            + "\n"
          );

        for i in range( 1, len(flds) ):

          r = line[i];

          for u in mw_cleanup( r ):

            j += 1;

            outf.write(
                "|"\
                 .join(
                      [ u,
                        u.upper(),
                        L[0].upper(),
                        str(j),
                        flds[i] ]
                    ) \
                + "\n"
              );
