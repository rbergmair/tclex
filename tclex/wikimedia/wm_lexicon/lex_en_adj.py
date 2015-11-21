__all__ \
  = [ "en_adj_bymeta",
      "en_adj_irregular_bycontent",
      "en_adj_regular_bycontent" ];


from txcrunch.wikimedia.wm.mw_cleanup import mw_cleanup;



def en_adj_bymeta( enwiktionary_en_word_bymeta_fn, out_fn ):

  cats \
    = {  50378: "",
         331429: "comparative",
         335705: "superlative",
         1629453: "positive",
         340845: "prespart",
         341967: "pastpart" };

  w = 0;

  with open( enwiktionary_en_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );
        catid = int(catid);

        if not ( ( pos == 'a' ) or ( catid in [ 340845, 341967 ] ) ):
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
        
        lemma = L[0];

        outf.write(
              ( "|"\
                 .join(
                      [ lemma,
                        lemma.upper(),
                        lemma.upper(),
                        '1',
                        cats.get(catid,"") ]
                    ) ) \
            + '\n'
          );

  return w;



def en_adj_irregular_bycontent( enwiktionary_en_adj_irregular_fn, out_fn ):

  w = 0;

  with open( enwiktionary_en_adj_irregular_fn, "rt" ) as inf:

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
        
        outf.write(
              "|".join( [ L[0],L[0].upper(),L[0].upper(),'1',"positive" ] ) \
            + "\n"
          );

        j = 1;
        for i in range(1,3):
          
          r = line[i];
          r = r.replace( "+", "" );
          r = r.replace( "[[", "" );
          r = r.replace( "]]", "" );
          
          pref = "";
          if i == 1 and r.startswith( "more " ):
            r = r[ len("more ") : ];
            pref = "mm";
          elif i == 2 and r.startswith( "most " ):
            r = r[ len("most ") : ];
            pref = "mm";
          
          for u in mw_cleanup( r ):
            j += 1;
            outf.write(
                  ( "|"\
                     .join(
                          [ u,
                            u.upper(),
                            L[0].upper(),
                            str(j),
                            ( None,
                              pref+"comparative",
                              pref+"superlative" )[ i ] ]
                        ) ) \
                + '\n'
              );

  return w;



def en_adj_regular_bycontent( enwiktionary_en_adj_regular_fn, out_fn ):

  w = 0;

  with open( enwiktionary_en_adj_regular_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      def out( rec ):

        outf.write( "|".join( [ str(x) for x in rec ] ) + '\n' );

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
        lemma = L[0];

        s = list( mw_cleanup( line[3] ) );
        if len(s) == 0:
          print( "WARNING! funky stem" );
          w += 1;
          continue;
        elif len(s) > 1:
          print( "WARNING! funky stem " + repr(s) );
          w += 1;
          continue;
        stem = s[0];

        atype = line[1];

        if atype == "-":

          out( [ stem,        stem.upper(),          lemma.upper(), 1, "positive"    ] );

        elif atype == "er":

          out( [ stem,        stem.upper(),          lemma.upper(), 1, "positive"    ] );
          out( [ stem+"er",   (stem+"er").upper(),   lemma.upper(), 2, "comparative" ] );
          out( [ stem+"est",  (stem+"est").upper(),  lemma.upper(), 3, "superlative" ] );

        elif atype == "ier":

          out( [ stem,        stem.upper(),          lemma.upper(), 1, "positive"    ] );
          out( [ stem+"ier",  (stem+"ier").upper(),  lemma.upper(), 2, "comparative" ] );
          out( [ stem+"iest", (stem+"iest").upper(), lemma.upper(), 3, "superlative" ] );

        elif atype == "mm":

          out( [ stem,        stem.upper(),          lemma.upper(), 1, "positive"      ] );
          out( [ stem,        stem.upper(),          lemma.upper(), 2, "mmcomparative" ] );
          out( [ stem,        stem.upper(),          lemma.upper(), 3, "mmsuperlative" ] );

        else:          

          print( "WARNING! " + repr( line ) );

  return w;
