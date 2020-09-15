## @file
## @brief Byte Code eXecution engine

from metaL import *

## @defgroup bcx BCX
## @ingroup samples
## @brief Byte Code eXecution engine
## https://github.com/ponyatov/bcx
## @{

class bcxModule(ccModule):

    def init_mk(self):
        super().init_mk()
        self.mk.obj // 'OBJ += bcx.bcx'
        self.mk.all.dropall()
        self.mk.all // '.PHONY: all'
        self.mk.all // 'all: bcx bcx.bcx' // '\t./$^'
        self.mk.rules // '%.bcx: asm %.4th' // '\t./$^'
        self.mk.sync()

    def init_apt(self):
        super().init_apt()
        self.apt // 'flex bison ragel'
        self.apt.sync()

    def init_gitignore(self):
        super().init_gitignore()
        self.gitignore.bot // '/asm'
        self.gitignore.sync()


MODULE = bcxModule('bcx')
diroot = MODULE['dir']

TITLE = Title('Byte Code eXecution engine')
MODULE['TITLE'] = TITLE

ABOUT = '''
Scripting & CLI engine: FORTH shell

* stack-based bytecode interpreter /ANSI C/
* targets for tiny embedded systems
  * microcontrollers
  * embedded Linux
  * tiny games
'''
MODULE['ABOUT'] = ABOUT

GITHUB = Url('https://github.com/ponyatov/')
GITHUB['branch'] = ''
MODULE['GITHUB'] = GITHUB

README = README(MODULE)
MODULE['dir'] // README
README.sync()

mk = MODULE['mk']

bcxc = MODULE.c
bcxh = MODULE.h
mk.src // ('BCX_C += %s' % bcxc.file())

asmh = hFile('asm', ext='.hpp')
mk.src // ('H += %s' % asmh.file())
diroot // asmh
asmh.top // ccInclude(bcxh)
parserh = hFile('parser')
mk.src // ('H += %s' % parserh.file())
lp = Section('lexer/parser', comment='//')
asmh.mid // lp
lp // 'extern int yylex();'
lp // 'extern char* yytext;'
lp // 'extern FILE* yyin;'
lp // 'extern int yyparse();'
lp // 'extern void yyerror(char*);'
lp // 'extern int yylineno;'
lp // ccInclude(parserh)
asmh.sync()

asmc = cFile('asm', ext='.cpp')
mk.src // ('ASM_C += %s' % asmc.file())
diroot // asmc
asmc.top // ccInclude(bcxh) // 'x'
err = Section('error', comment='//')
asmc.bot // err
YYERR = r'"\n\n#%i: %s [%s]\n\n",yylineno,yytext'
err //\
    'void yyerror(char *msg) {' //\
    f'\tfprintf(stdout,{YYERR});' //\
    f'\tfprintf(stderr,{YYERR});' //\
    '\texit(-1);' //\
    '}'
asmc.sync()

syntax_header = '''
%%{
    %s
%%}
''' % ccInclude(asmh).file()

lexerc = cFile('lexer')
mk.src // ('ASM_C += %s' % lexerc.val)
MODULE['gitignore'].mid // lexerc
mk.rules // '%.c: %.lex\n\tflex -o $@ $<'

lex = File('lexer.lex', comment='')
diroot // lex
lex // syntax_header
lex // '%option noyywrap yylineno'
lex // '%%'
lex // '. ANY'
lex.sync()

parserc = cFile('parser')
mk.src // ('ASM_C += %s' % parserc.file())
MODULE['gitignore'].mid // parserc // parserh
mk.rules // '%.c: %.yacc\n\tbison -o $@ $<'

yacc = File('parser.yacc', comment='//')
diroot // yacc
yacc // syntax_header
yacc // '''
%defines %union { char c; }
%%
REPL :
'''
yacc.sync()

mk.rules //\
    'asm: $(ASM_C) $(H)' //\
    '\t$(CXX) $(CFLAGS) -o $@ $(ASM_C)'
mk.rules //\
    'bcx: $(BCX_C) $(H)' //\
    '\t$(CC) $(CFLAGS) -o $@ $(BCX_C)'

mk.sync()
MODULE['gitignore'].sync()

bcxc.bot // 'int main(int argc, char *argv[]){'
bcxc.bot // '\tassert(argc==2);'
bcxc.bot // '\treturn 0;'
bcxc.bot // '}'
bcxc.sync()

asmc.bot // 'int main(int argc, char *argv[]){'
asmc.bot // '\tassert(argc==2);'
asmc.bot // '\tyyin = fopen(argv[1],"r"); if (!yyin) abort();'
asmc.bot // '\treturn yyparse();'
asmc.bot // '}'
asmc.sync()

bcx = File('bcx.4th', comment='\\')
diroot // bcx
bcx.sync()

## @}
