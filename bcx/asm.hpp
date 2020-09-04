
// \ <section:top>
// powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
// @file
#ifndef _ASM_H
#include <stdint.h>
#include <bcx.h>
// / <section:top>
// \ <section:mid>

// \ <section:lexer/parser>
extern int yylex();
extern char* yytext;
extern FILE* yyin;
extern int yyparse();
extern void yyerror(char*);
extern int yylineno;
#include <parser.h>
// / <section:lexer/parser>
// / <section:mid>
// \ <section:bot>
#endif // _ASM_H
// / <section:bot>