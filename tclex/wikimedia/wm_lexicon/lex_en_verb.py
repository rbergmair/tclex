__all__ \
  = [ "en_verb_bymeta",
      "en_verb_regular_bycontent",
      "en_verb_irregular_bycontent" ];


from txcrunch.wikimedia.wm.mw_cleanup import mw_cleanup;
from txcrunch.wikimedia.wm.mw_cleanup import mw_unescape;



def en_verb_bymeta( enwiktionary_en_word_bymeta_fn, out_fn ):

  cats \
    = {  50375: "",
        741288: "press3sg",
        195330: "ident",
        341967: "past",
        793788: "press2sg" };

  w = 0;

  with open( enwiktionary_en_word_bymeta_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        ( lemma, pos, catid ) = line.split( "|" );

        if pos != 'v':
          continue;

        catid = int( catid );
        
        if not catid in cats:
          print( "WARNING! " + str(catid) );
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



def en_verb_regular_bycontent( enwiktionary_en_verb_regular_fn, out_fn ):

  w = 0;

  with open( enwiktionary_en_verb_regular_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      def out( rec ):

        outf.write( "|".join( [ str(x) for x in rec ] ) + '\n' );

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        line = line.split( "|" );

        L = list( mw_cleanup( line[0] ) );
        if len(L) == 0:
          print( "WARNING! funky lemma" + repr(L) );
          w += 1;
          continue;
        elif len(L) > 1:
          print( "WARNING! funky lemma " + repr(L) );
          w += 1;
          continue;

        lemma = L[0];

        vtype = line[1];
        
        stem = mw_unescape( line[2] );
        tchar = mw_unescape( line[3] );

        out( [ lemma, lemma.upper(), lemma.upper(), "1", "inf" ] );
       
        if vtype == "s":
          
          out( [ lemma + "s",          (lemma + "s").upper(),        lemma.upper(), 2, "press3sg" ] );
          out( [ stem+tchar + "ing",   (stem+tchar + "ing").upper(), lemma.upper(), 3, "preprog" ] );
          out( [ stem+tchar + "ed",    (stem+tchar + "ed").upper(),  lemma.upper(), 4, "past" ] );
          out( [ stem+tchar + "ed",    (stem+tchar + "ed").upper(),  lemma.upper(), 5, "ppart" ] );

        elif vtype == "es":
          
          out( [ stem+tchar + "es",    (stem+tchar + "es").upper(),  lemma.upper(), 2, "press3sg" ] );
          out( [ stem+tchar + "ing",   (stem+tchar + "ing").upper(), lemma.upper(), 3, "preprog" ] );
          out( [ stem+tchar + "ed",    (stem+tchar + "ed").upper(),  lemma.upper(), 4, "past" ] );
          out( [ stem+tchar + "ed",    (stem+tchar + "ed").upper(),  lemma.upper(), 5, "ppart" ] );

        elif vtype == "d":

          out( [ lemma + "s",          (lemma + "s").upper(),        lemma.upper(), 2, "press3sg" ] );
          out( [ stem+tchar + "ing",   (stem+tchar + "ing").upper(), lemma.upper(), 3, "preprog" ] );
          out( [ stem+tchar + "d",     (stem+tchar + "d").upper(),   lemma.upper(), 4, "past" ] );
          out( [ stem+tchar + "d",     (stem+tchar + "d").upper(),   lemma.upper(), 5, "ppart" ] );

        elif vtype == "ing":
          
          if tchar:
            out( [ lemma + "s",        (lemma + "s").upper(),        lemma.upper(), 2, "press3sg" ] );
            out( [ stem+tchar + "ing", (stem+tchar + "ing").upper(), lemma.upper(), 3, "preprog" ] );
            out( [ lemma + "d",        (lemma + "d").upper(),        lemma.upper(), 4, "past" ] );
            out( [ lemma + "d",        (lemma + "d").upper(),        lemma.upper(), 5, "ppart" ] );
            
          else:
            out( [ lemma + "s",        (lemma + "s").upper(),        lemma.upper(), 2, "press3sg" ] );
            out( [ stem+tchar + "ing", (stem+tchar + "ing").upper(), lemma.upper(), 3, "preprog" ] );
            out( [ stem+tchar + "ed",  (stem+tchar + "ed").upper(),  lemma.upper(), 4, "past" ] );
            out( [ stem+tchar + "ed",  (stem+tchar + "ed").upper(),  lemma.upper(), 5, "ppart" ] );

        elif vtype == "ed":
          
          out( [ stem+tchar + "es",    (stem+tchar + "es").upper(),  lemma.upper(), 2, "press3sg" ] );
          out( [ lemma  + "ing",       (lemma  + "ing").upper(),     lemma.upper(), 3, "preprog" ] );
          out( [ stem+tchar + "ed",    (stem+tchar + "ed").upper(),  lemma.upper(), 4, "past" ] );
          out( [ stem+tchar + "ed",    (stem+tchar + "ed").upper(),  lemma.upper(), 5, "ppart" ] );
        
        else:
          
          print( "WARNING! " + repr( (lemma,vtype,stem,tchar) ) );

  return w;



def en_verb_irregular_bycontent( enwiktionary_en_verb_irregular_fn, out_fn ):

  w = 0;

  with open( enwiktionary_en_verb_irregular_fn, "rt" ) as inf:

    with open( out_fn, "at" ) as outf:

      for line in inf:

        if line and line[ -1 ] == '\n':
          line = line[ :-1 ];

        line = line.split( "|" );

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
            "|"\
             .join(        
                [ L[0], L[0].upper(), L[0].upper(), "1", "inf" ]
              )
            + "\n"
          );

        j = 1;
        
        for i in range(1,5):
          
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
                        ( "", "press3sg", "preprog", "past", "ppart" )[ i ] ]
                    ) \
                + "\n"
              );

  return w;
