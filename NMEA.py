
from metaL import *

class thisModule(cModule):

    def __init__(self, V=None):
        super().__init__(V)
        cModule.mixin_ragel(self)

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f12.cmd.val = 'make all'
        self.vscode.settings.sync()

    def init_skelex(self):
        pass

    def init_mk(self):
        super().init_mk()
        self.mk.test.targets // ' sample.nmea'
        self.mk.test.dropall() // '$^ | head -n22'
        self.mk.sync()


MODULE = thisModule()

TITLE = Title('NMEA 0183 parser')
MODULE['TITLE'] = MODULE.TITLE = TITLE

ABOUT = '''
* https://github.com/szhukovks/ragel-parser
  * https://www.colm.net/files/ragel/ragel-guide-6.3.pdf
  * http://thingsaaronmade.com/blog/a-simple-intro-to-writing-a-lexer-with-ragel.html
* Erlang/Elixir
  * https://github.com/joshnuss/nmea
  * https://github.com/bryanjos/geo
* https://en.wikipedia.org/wiki/NMEA_0183
  * ru
    * http://wiki.amperka.ru/articles:gps:nmea
'''
MODULE['ABOUT'] = MODULE.ABOUT = ABOUT

README = README(MODULE)
MODULE['dir'] // README
README.sync()

c = MODULE.c
ragel = MODULE.ragel

ragel.rex //\
        r'''
    comment  = '#'[^\r\n]*;

    conventional =       '$'         >{s=p;} @{token("conventional",s,p+1);}       ;
    special      =       '!'         >{s=p;} @{token("special"     ,s,p+1);}       ;
    crc          = '*' ( [0-9A-F]{2} >{s=p;} @{token("crc"         ,s,p+1);} )     ;
    nmeatoken    =     ( [A-Z]+      >{s=p;} @{token("nmeatoken"   ,s,p+1);} ) ',' ;

    generic =
        (conventional|special)
        (nmeatoken [^\r\n]+    >{crc_count=0;} ${crc_count ^= *p;}                                                      )
        (crc                                                       @{printf("\ncrc check: crc_count= %.2x",crc_count);} )
    ;
        ''' 
#         (S(f'{MODULE} := |*', '*|;') //
ragel.scan //\
            r'comment  => {token("comment" ,ts,te);};' //\
            r'generic => {token("generic",ts,te);};'

ragel.bot // r'''
void token(char *name, unsigned char *ts, unsigned char *te) {
    assert(ts); assert(te); assert(ts<=te);
    printf("\n%s:{",name);
    printf(" %x %x ",ts,te);
    for (unsigned char *c=ts;c<te;c++)
        printf("%c",*c);
    printf("}");
}'''

ragel.mid //\
    (S('void parse(unsigned char *p, unsigned char *pe) {', '}') //
        'assert(p<pe);'//
        r'printf("\nchars:%i",pe-p);'//
        '%%write data;' //
        r'''
        unsigned char* ts  = (unsigned char*) NULL;
        unsigned char* te  = ts;
        unsigned char*  s  = p;
        unsigned char* eof = pe;
        unsigned int
            cs  = NMEA_start,
            act = 0;

        uint8_t crc_count  = 0;
        ''' //
        '%%write init;' //
        '%%write exec;'
     )


ragel.sync()


main // r'''
// open file
  assert(argc == 2);
  for (int i = 0; i < argc; i++)
    printf("\nargv[%i] = <%s>", i, argv[i]);
  FILE *fh = fopen(argv[1], "r"); assert(fh);

// scan loop
  unsigned char *line_buf = NULL;
  ssize_t line_size = 0;
  size_t line_buf_size = 0;
  #define LSZ (line_size = getline(&line_buf, &line_buf_size, fh))
  for (LSZ; line_size >= 0; LSZ) {
    // printf("\nline size:%i", line_size);
    parse(&line_buf[0],&line_buf[line_size]);
    // printf("\n");
  }

// close session
  fclose(fh);
  free(line_buf);
'''

c.bot // main
c.sync()

nmea = File('sample', ext='.nmea', comment='#')
MODULE['dir'] // nmea
nmea // '''

# @vertexod
$GPGGA,172814.0,3723.46587704,N,12202.26957864,W,2,6,1.2,18.893,M,-25.669,M,2.0,0031*4F

# http://wiki.amperka.ru/articles:gps:nmea
$GPGGA,123519,4807.038,N,01131.000,E,1,08,0.9,545.4,M,46.9,M,,*47
$GPRMC,123519,A,4807.038,N,01131.000,E,022.4,084.4,230394,003.1,W*6A
$PMTK251,9600*17

# https://en.wikipedia.org/wiki/NMEA_0183

# https://github.com/joshnuss/nmea/blob/master/test/nmea_test.exs
$GPGSV,3,1,12,01,,,23,02,,,23,03,,,22,05,,,23*7C

# https://github.com/joshnuss/nmea
$GPGGA,092750.000,5321.6802,N,00630.3372,W,1,8,1.03,61.7,M,55.2,M,,*76
$GPGSA,A,3,10,07,05,02,29,04,08,13,,,,,1.72,1.03,1.38*0A
$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70
$GPGSV,3,2,11,02,39,223,19,13,28,070,17,26,23,252,,04,14,186,14*79
$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76
$GPRMC,092750.000,A,5321.6802,N,00630.3372,W,0.02,31.66,280511,,,A*43
$GPGGA,092751.000,5321.6802,N,00630.3371,W,1,8,1.03,61.7,M,55.3,M,,*75
$GPGSA,A,3,10,07,05,02,29,04,08,13,,,,,1.72,1.03,1.38*0A
$GPGSV,3,1,11,10,63,137,17,07,61,098,15,05,59,290,20,08,54,157,30*70
$GPGSV,3,2,11,02,39,223,16,13,28,070,17,26,23,252,,04,14,186,15*77
$GPGSV,3,3,11,29,09,301,24,16,09,020,,36,,,*76
$GPRMC,092751.000,A,5321.6802,N,00630.3371,W,0.06,31.66,280511,,,A*45
'''
nmea.sync()

os.system(f'cd {MODULE} ; make ragel')
