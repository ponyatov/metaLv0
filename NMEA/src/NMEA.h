// powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
// \ <section:top>
#ifndef _NMEA_H
#include <stdlib.h>
#include <stdio.h>
#include <assert.h>
// / <section:top>
// \ <section:mid>
extern void parse(unsigned char *p , unsigned char *pe);
extern void token(char *name, unsigned char *ts, unsigned char *te);
// / <section:mid>
// \ <section:bot>
#endif // _NMEA_H
// / <section:bot>
