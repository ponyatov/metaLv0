## @file
## @brief ANSI C'99 code generation targeted for @ref tcc

from metaL import *

## @defgroup cc ANSI C'99
## @ingroup gen
## @brief ANSI C'99 code generation targeted for @ref tcc

## @ingroup cc
class CC(Object):
    pass

## @ingroup cc
## C'99 syntax file (`.c`/`.h`)
class ccFile(CC, File):
    def __init__(self, V, comment='//'):
        File.__init__(self, V, comment)

## @ingroup cc
## `@include`
class cInclude(CC):
    def file(self): return '#include <%s.h>' % self.val

## @ingroup cc
class ccModule(CC, anyModule):
    def __init__(self, V=None):
        anyModule.__init__(self, V)
        # apt.txt
        self.apt // 'binutils tcc' // 'libc6-dev'
        self.apt.sync()
        # .c/.h
        self.c = self['c'] = ccFile('%s.c' % self.val)
        self.h = self['h'] = ccFile('%s.h' % self.val)
        self.diroot // self.c // self.h
        # .c
        self.c.head // ('#include "%s.h"' % self.val)
        self.c.tail // 'main(){}'
        self.c.sync()
        # .h
        self.h.head // ('#ifndef _H_%s\n#define _H_%s' % (self.val, self.val))
        self.h.head // cInclude('stdint') // cInclude('stdlib')
        self.h.tail // ('#endif // _H_%s' % self.val)
        self.h.sync()
        # Makefile
        self.mk.body // '.PHONY: all repl'
        self.mk.body // 'all: repl'
        self.mk.body // ('repl: ./%s\n\t./$^' % self.val)
        # ('all: repl\nrepl: %s.c %s.h\n\ttcc -o $@ $<' % (self.val, self.val))
        self.mk.sync()
        # .gitignore
        self.gitignore.body // ('%s\n%s.exe' % (self.val, self.val)) // '*.o'
        self.gitignore.sync()


MODULE = ccModule()

class ccType(CC, Meta):
    pass

# main = Fn('main')
# main >> Vector('args')
# main


# class Int(Type): pass
# class Char(Type): pass
# class Array(Type): pass
# class Ptr(Type): pass

# main['args'] // Int('argc')
# argv = (Array('')//(Ptr('')//Char('argv')))
# main['args'] // argv
