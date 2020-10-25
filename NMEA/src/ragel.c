
#line 1 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
// powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
// \ <section:top>
#include <NMEA.h>
// / <section:top>
// \ <section:mid>

#line 30 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"

void parse(unsigned char *p, unsigned char *pe) {
    assert(p<pe);
    printf("\nchars:%i",pe-p);
    
#line 16 "/home/ponyatov/metaL/NMEA/src/ragel.c"
static const int NMEA_start = 8;
static const int NMEA_first_final = 8;
static const int NMEA_error = 0;

static const int NMEA_en_NMEA = 8;


#line 35 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
    
        unsigned char* ts  = (unsigned char*) NULL;
        unsigned char* te  = ts;
        unsigned char*  s  = p;
        unsigned char* eof = pe;
        unsigned int
            cs  = NMEA_start,
            act = 0;

        uint8_t crc_count  = 0;
        
    
#line 37 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	{
	cs = NMEA_start;
	ts = 0;
	te = 0;
	act = 0;
	}

#line 47 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
    
#line 47 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	{
	if ( p == pe )
		goto _test_eof;
	switch ( cs )
	{
tr0:
#line 28 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{te = p+1;{token("eol",ts,ts);}}
	goto st8;
tr6:
#line 1 "NONE"
	{	switch( act ) {
	case 0:
	{{goto st0;}}
	break;
	case 2:
	{{p = ((te))-1;}token("generic",ts,te);}
	break;
	}
	}
	goto st8;
tr15:
#line 27 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{te = p;p--;{token("generic",ts,te);}}
	goto st8;
tr16:
#line 26 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{te = p;p--;{token("comment" ,ts,te);}}
	goto st8;
st8:
#line 1 "NONE"
	{ts = 0;}
#line 1 "NONE"
	{act = 0;}
	if ( ++p == pe )
		goto _test_eof8;
case 8:
#line 1 "NONE"
	{ts = p;}
#line 87 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	switch( (*p) ) {
		case 10u: goto tr0;
		case 13u: goto st1;
		case 33u: goto tr12;
		case 35u: goto st10;
		case 36u: goto tr14;
	}
	goto st0;
st0:
cs = 0;
	goto _out;
st1:
	if ( ++p == pe )
		goto _test_eof1;
case 1:
	if ( (*p) == 10u )
		goto tr0;
	goto st0;
tr12:
#line 15 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{s=p;}
#line 15 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{token("special"     ,s,p+1);}
	goto st2;
tr14:
#line 14 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{s=p;}
#line 14 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{token("conventional",s,p+1);}
	goto st2;
st2:
	if ( ++p == pe )
		goto _test_eof2;
case 2:
#line 122 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	if ( 65u <= (*p) && (*p) <= 90u )
		goto tr2;
	goto st0;
tr2:
#line 17 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{s=p;}
#line 17 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{token("nmeatoken"   ,s,p+1);}
	goto st3;
tr4:
#line 17 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{token("nmeatoken"   ,s,p+1);}
	goto st3;
st3:
	if ( ++p == pe )
		goto _test_eof3;
case 3:
#line 140 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	if ( (*p) == 44u )
		goto st4;
	if ( 65u <= (*p) && (*p) <= 90u )
		goto tr4;
	goto st0;
st4:
	if ( ++p == pe )
		goto _test_eof4;
case 4:
	switch( (*p) ) {
		case 10u: goto st0;
		case 13u: goto st0;
	}
	goto tr5;
tr5:
#line 21 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{crc_count=0;}
#line 21 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{crc_count ^= *p;}
	goto st5;
tr7:
#line 21 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{crc_count ^= *p;}
	goto st5;
st5:
	if ( ++p == pe )
		goto _test_eof5;
case 5:
#line 169 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	switch( (*p) ) {
		case 10u: goto tr6;
		case 13u: goto tr6;
		case 42u: goto tr8;
	}
	goto tr7;
tr8:
#line 21 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{crc_count ^= *p;}
	goto st6;
st6:
	if ( ++p == pe )
		goto _test_eof6;
case 6:
#line 184 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	switch( (*p) ) {
		case 10u: goto tr6;
		case 13u: goto tr6;
		case 42u: goto tr8;
	}
	if ( (*p) > 57u ) {
		if ( 65u <= (*p) && (*p) <= 70u )
			goto tr9;
	} else if ( (*p) >= 48u )
		goto tr9;
	goto tr7;
tr9:
#line 21 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{crc_count ^= *p;}
#line 16 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{s=p;}
	goto st7;
st7:
	if ( ++p == pe )
		goto _test_eof7;
case 7:
#line 206 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	switch( (*p) ) {
		case 10u: goto tr6;
		case 13u: goto tr6;
		case 42u: goto tr8;
	}
	if ( (*p) > 57u ) {
		if ( 65u <= (*p) && (*p) <= 70u )
			goto tr10;
	} else if ( (*p) >= 48u )
		goto tr10;
	goto tr7;
tr10:
#line 1 "NONE"
	{te = p+1;}
#line 21 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{crc_count ^= *p;}
#line 16 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{token("crc"         ,s,p+1);}
#line 22 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{printf("\ncrc check: crc_count= %.2x",crc_count);}
#line 27 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
	{act = 2;}
	goto st9;
st9:
	if ( ++p == pe )
		goto _test_eof9;
case 9:
#line 234 "/home/ponyatov/metaL/NMEA/src/ragel.c"
	switch( (*p) ) {
		case 10u: goto tr15;
		case 13u: goto tr15;
		case 42u: goto tr8;
	}
	goto tr7;
st10:
	if ( ++p == pe )
		goto _test_eof10;
case 10:
	switch( (*p) ) {
		case 10u: goto tr16;
		case 13u: goto tr16;
	}
	goto st10;
	}
	_test_eof8: cs = 8; goto _test_eof; 
	_test_eof1: cs = 1; goto _test_eof; 
	_test_eof2: cs = 2; goto _test_eof; 
	_test_eof3: cs = 3; goto _test_eof; 
	_test_eof4: cs = 4; goto _test_eof; 
	_test_eof5: cs = 5; goto _test_eof; 
	_test_eof6: cs = 6; goto _test_eof; 
	_test_eof7: cs = 7; goto _test_eof; 
	_test_eof9: cs = 9; goto _test_eof; 
	_test_eof10: cs = 10; goto _test_eof; 

	_test_eof: {}
	if ( p == eof )
	{
	switch ( cs ) {
	case 5: goto tr6;
	case 6: goto tr6;
	case 7: goto tr6;
	case 9: goto tr15;
	case 10: goto tr16;
	}
	}

	_out: {}
	}

#line 48 "/home/ponyatov/metaL/NMEA/src/NMEA.ragel"
}
// / <section:mid>
// \ <section:bot>

void token(char *name, unsigned char *ts, unsigned char *te) {
    assert(ts); assert(te); assert(ts<=te);
    printf("\n%s:{",name);
    printf(" %x %x ",ts,te);
    for (unsigned char *c=ts;c<te;c++)
        printf("%c",*c);
    printf("}");
}
// / <section:bot>
