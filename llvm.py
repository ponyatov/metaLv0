## @file
## @brief LLVM hacking

from metaL import *

## @defgroup ll LLVM
## @ingroup gen
## @brief low-level portable assembly
## @{

class LL(Object):
    pass

## LLVM assembly file (`.ll`)
class llFile(LL, File):
    def __init__(self, V, comment=';'):
        super().__init__(V + '.ll', comment)

## @name types
## @{

## type
class llType(LL):
    def file(self): return self.val


i32 = llType('i32')

## @}

## function
class llFn(LL, Fn):
    def __init__(self, returns, name):
        super().__init__(name)
        self['ret'] = returns

    def file(self):
        ret = '\ndefine %s @%s() {' % (self['ret'].file(), self.val)
        ret += '\n\tret %s 0\n}' % self['ret'].file()
        return ret


class llModule(LL, anyModule):
    def __init__(self, V=None):
        super().__init__(V)
        self.hello = File('hello.ll')

    def init_apt(self):
        super().init_apt()
        self.apt // 'llvm-7 clang-7 lldb-7'
        self.apt.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.tools // 'OBJDUMP = LANG=C objdump'
        self.mk.tools // 'CLANG   = LANG=C clang'
        self.mk.tools // 'LLC     = LANG=C llc'
        self.mk.tools // 'CC      = $(CLANG)'
        self.mk.all // '.PHONY: all'
        self.mk.all // 'all: $(MODULE)'
        self.mk.all // '$(MODULE): $(OBJ) $(SRC)'
        self.mk.all // '\t$(CC) -o $@ $(OBJ)'
        # self.mk.all // '\t$(OBJDUMP) -x $@ > $@.objdump'
        self.mk.rules // '%.ll: %.c'
        self.mk.rules // '\t$(CLANG) -O0 -S -emit-llvm -o $@ $<'
        self.mk.rules // '%.s: %.ll'
        self.mk.rules // '\t$(LLC) -O0 -o $@ $<'
        self.mk.rules // '%.o: %.s'
        self.mk.rules // '\t$(CLANG) -c -o $@ $<'
        self.mk.rules // '%.objdump: %.o'
        self.mk.rules // '\t$(OBJDUMP) -x $< > $@'
        self.mk.src // 'SRC += $(MODULE).objdump'
        self.mk.mid // '$(MODULE).objdump: $(MODULE)'
        self.mk.mid // '\t$(OBJDUMP) -x $< > $@'
        self.mk.sync()

    def init_gitignore(self):
        super().init_gitignore()
        self.gitignore.mid // '*.ll' // '*.s' // '*.bc'
        self.gitignore.sync()


MODULE = llModule()

TITLE = 'demonstrates some low-level programming'
MODULE['TITLE'] = TITLE

ABOUT = '''
This module shows some elements of `metaL` programming which are more
compiler-specific.

* working with elementary code elements
* using LLVM as a portable assembly
* powered by `metaL`
'''
MODULE['ABOUT'] = ABOUT

diroot = MODULE.diroot

README = README(MODULE)
diroot // README
README.sync()

def src(fileclass, name):
    srcfile = fileclass(name)
    exts = ['ll', 's', 'objdump']
    if fileclass == ccFile:
        exts += ['c']
    fset = map(lambda x: '%s.%s' % (name, x), exts)
    MODULE.mk.src // ('SRC += %s' % ' '.join(fset))
    MODULE.mk.obj // ('OBJ += %s.o' % name)
    diroot // srcfile
    return srcfile


empty = src(ccFile, 'empty')
empty.sync()

hello = src(ccFile, 'hello')
hello.mid // 'int main(){}'
hello.sync()

ll = src(llFile, 'll')
ll.mid // llFn(i32, 'foo')
ll.sync()

MODULE.mk.sync()

## @}
