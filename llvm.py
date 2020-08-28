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
    def file(self): return '%s %s' % (self.ll_type(), self.ll_val())
    ## LLVM type (without first `ll` prefix)
    def ll_type(self): return self._type()[2:]
    ## object value
    def ll_val(self): return '%s' % self.val
    ## return object used in Fn.args
    def ll_arg(self): return self.file()

class llI32(llType):
    def cc_type(self): return 'int32_t'


i32 = llI32(0)

class llVoid(llType):
    def ll_arg(self): return self._val()


void = llVoid('')

## @}

## function
class llFn(LL, Fn):
    def __init__(self, name, args=void, returns=void):
        super().__init__(name)
        self['args'] = args
        self['ret'] = returns

    def file(self):
        ret = '\ndefine %s @%s(%s) {' % (self['ret'].ll_type(),
                                         self.val, self['args'].ll_arg())
        for j in self.nest:
            ret += '\n%s' % j.file()
        ret += '\n\tret %s\n}' % self['ret'].file()
        return ret

    def cc_arg(self): return self.ll_arg()
    def ll_arg(self): return self._val()
    # def ll_ret(self):
    #     return '\tret %s' % self['ret'].file()

    def cc_call(self): return '%s()' % self._val()

    def cc_extern(self):
        ret = '\nextern %s %s(' % (self['ret'].cc_type(),self.val)
        ret += self['args'].cc_type()
        ret += ');'
        return ret


class llModule(LL, anyModule):
    def __init__(self, V=None):
        super().__init__(V)
        self.hello = File('hello.ll')

    def init_apt(self):
        super().init_apt()
        self.apt // 'llvm-7 clang-7 lldb-7'
        self.apt // 'wabt'
        self.apt.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.tools // 'OBJDUMP = LANG=C objdump'
        self.mk.tools // 'CLANG   = LANG=C clang'
        self.mk.tools // 'LLC     = LANG=C llc'
        self.mk.tools // 'CC      = $(CLANG)'
        self.mk.all // '.PHONY: all'
        self.mk.all // 'all: $(MODULE)'
        self.mk.all // '\t./$^'
        self.mk.all // '$(MODULE): $(OBJ) $(SRC) $(WASM)'
        self.mk.all // '\t$(CC) -o $@ $(OBJ)'
        # self.mk.all // '\t$(OBJDUMP) -x $@ > $@.objdump'
        self.mk.rules // '%.ll: %.c'
        self.mk.rules // '\t$(CLANG) -S -emit-llvm -o $@ $<'
        self.mk.rules // '%.s: %.ll'
        self.mk.rules // '\t$(LLC) -o $@ $<'
        self.mk.rules // '%.o: %.s'
        self.mk.rules // '\t$(CLANG) -c -o $@ $<'
        self.mk.rules // '%.wasm: %.ll'
        self.mk.rules // '\t$(LLC) -march=wasm32 -filetype=obj -o $@ $<'
        self.mk.rules // '\twasm-objdump -dx $@ > $@.objdump'
        self.mk.rules // '%.objdump: %.o'
        self.mk.rules // '\t$(OBJDUMP) -dx $< > $@'
        self.mk.src // 'SRC += $(MODULE).objdump'
        self.mk.mid // '$(MODULE).objdump: $(MODULE)'
        self.mk.mid // '\t$(OBJDUMP) -dx $< > $@'
        self.mk.sync()

    def init_gitignore(self):
        super().init_gitignore()
        self.gitignore.mid // '*.ll' // '*.s' // '*.bc' // '*.wasm'
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

mk = MODULE.mk

def src(fileclass, name):
    srcfile = fileclass(name)
    exts = ['ll', 's', 'objdump']
    if fileclass == ccFile:
        exts += ['c']
    fset = map(lambda x: '%s.%s' % (name, x), exts)
    mk.src // ('SRC += %s' % ' '.join(fset))
    mk.obj // ('OBJ += %s.o' % name)
    diroot // srcfile
    return srcfile


empty = src(ccFile, 'empty')
empty.sync()

a = llI32('%a')
foo = llFn('foo', a, a)

hello = src(ccFile, 'hello')
hello.top // foo.cc_extern()
main = ccFn('main', returns=ccint)#'int main(int argc, char *argv[]){'
hello.mid // main
printf = ccFn('printf', Vector() // "foo:%i\\n" // foo)
main // printf #''\tprintf(, foo(123));'
hello.sync()

ll = src(llFile, 'll')
ll.mid // foo
ll.mid // llFn('bar')
ll.sync()

mk.obj // 'WASM += ll.wasm'
mk.sync()

## @}
