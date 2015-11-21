__all__ \
  = [ "de_noun_bymeta" ];


from tclex.wikimedia.wm.mw_cleanup import mw_cleanup;



def de_noun_bymeta( dewiktionary_de_word_bymeta_fn, out_fn ):

  cats \
    = { 108024: "",
        542337: "",
        542338: "",
        542339: "",
         57754: "",
         92334: "nomsg",
         92374: "nompl" };

  w = 0;

  with open( dewiktionary_de_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );

        if pos != 'n':
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
            "|"\
             .join(        
                [ L[0], L[0].upper(), L[0].upper(), "1", cats[catid] ]
              )
            + "\n"
          );



def de_noun_bycontent( dewiktionary_de_noun_table_fn, out_fn ):

  artikel \
    = [ "DAS", "DAS/DEN", "DAS/DER", "DAS/DIE",
        "DEM", "DEM/DER",
        "DEN", "DEN/DAS", "DEN/DAS/DIE", "DEN/DIE",
        "DER", "DER/DAS", "DER/DAS/DIE", "DER/DEM", "DER/DIE",
        "DES", "DES/DER",
        "DIE", "DIE/DAS" ];

  flds \
    = [ "lemma",
        "nomsg", "gensg", "datsg", "accsg",
        "nompl", "genpl", "datpl", "accpl" ];    

  w = 0;

  with open( dewiktionary_de_noun_table_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        line = line.split( '|' );

        L = list( mw_cleanup( line[0], artikel ) );

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

          for u in mw_cleanup( r, artikel ):

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
