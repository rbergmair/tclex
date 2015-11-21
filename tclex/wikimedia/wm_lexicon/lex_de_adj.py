__all__ \
  = [ "de_adj_bymeta" ];


from tclex.wikimedia.wm.mw_cleanup import mw_cleanup;



def de_adj_bymeta( dewiktionary_de_word_bymeta_fn, out_fn ):

  cats \
    = { 543158: "positive",    
        543160: "",
         57756: "",
         58731: "",
         61254: "" };

  w = 0;

  with open( dewiktionary_de_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );

        if pos != 'a':
          continue;

        catid = int(catid);

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
              ( "|"\
                 .join(
                      [ L[0],
                        L[0].upper(),
                        L[0].upper(),
                        '1',
                        cats.get(catid,"") ]
                    ) ) \
            + '\n'
          );

  return w;



def de_adj_bycontent( dewiktionary_de_adj_table_fn, out_fn ):

  beiworte = [ "AM" ];

  flds = [ "lemma", "positive", "comparative", "superlative" ];

  w = 0;

  with open( dewiktionary_de_adj_table_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        line = line.split( '|' );

        L = list( mw_cleanup( line[0], beiworte ) );

        if len(L) == 0:
          print( "WARNING! funky lemma" );
          w += 1;
          continue;
        elif len(L) > 1:
          print( "WARNING! funky lemma " + repr(L) );
          w += 1;
          continue;

        j = 0;

        for i in range( 1, len(flds) ):

          r = line[i];

          for u in mw_cleanup( r, beiworte ):

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
  
  return w;
