
// \ <section:top>
// powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
// @file
#include <asm.h>
#include <bcx>
// / <section:top>
// \ <section:mid>
// / <section:mid>
// \ <section:bot>

// \ <section:error>
void yyerror(char *msg) {
	fprintf(stdout,"\n\n#%i: %s [%s]\n\n",yylineno,yytext);
	fprintf(stderr,"\n\n#%i: %s [%s]\n\n",yylineno,yytext);
	exit(-1);
}
// / <section:error>
int main(int argc, char *argv[]){
	assert(argc==2);
	yyin = fopen(argv[1],"r"); if (!yyin) abort();
	return yyparse();
}
// / <section:bot>