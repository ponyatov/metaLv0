## @file
## @brief generic ANSI/GNU C'99

from metaL import *

## @defgroup cc C99
## @ingroup gen
## @brief code generation targeted for @ref tcc

## @ingroup cc
class cFile(File):
    def __init__(self, V, comment='//'):
        File.__init__(self, V, comment)

## @ingroup cc
class ccModule(anyModule):
    pass

hello = ccModule()

class ccType(Meta):
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
