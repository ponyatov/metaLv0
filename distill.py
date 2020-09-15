## @file
## @brief Distilled `metaL` / SICP chapter 4 /

from metaL import *

## @defgroup distill distill
## @ingroup samples
## @brief Distilled `metaL` / SICP chapter 4 /
## https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d
## @{

## metaL core implementation
py = pyFile('metaL')

## metaL core tests
test = pytestFile(py)

## inherit special Module type for metaLayer-based projects
class meModule(minpyModule):

    ## @param[in] V by default `pyModule` uses current `__file__` for module naming
    def __init__(self, V=None):
        # most Python project setup will be done by a parent `pyModule` constructor
        super().__init__(V)

    ## will be called by `super().__init__` to generate `metaL.py`
    def init_py(self):
        ## module master `.py` `File`
        self.py = py
        self['py'] = self.py
        # ## module tests
        self.test = test
        self['test'] = self.test
        self.test.mid // ('from %s import *' % py.val)
        # module (project) root `Dir`ectory
        self.diroot // self.py // self.test
        # `File` does not reflects on disk until direct `.sync()` call is done
        self.py.sync()
        self.test.sync()

    ## patch default `Makefile` from `pyModule` with REPL
    def init_mk(self):
        super().init_mk()
        # force module name
        self.mk.module.dropall() // (f'{"MODULE":<8} = {py}')
        # build Makefile/all section with REPL pattern
        self.mk.all //\
            '.PHONY: all' //\
            'all: repl' //\
            '.PHONY: repl' //\
            (S('repl: $(PYT) $(PY) %s' % py.file()) //
                ('$(PYT) %s' % test.file()) //
                ('$(PY) -i %s' % py.file()) //
                '$(MAKE) $@'
             )
        self.mk.sync()

    def init_reqs(self):
        super().init_reqs()
        (self.reqs // 'pytest').sync()

    def init_vscode_launch(self):
        super().init_vscode_launch()
        self.vscode.launch.program[0] = '"program": "%s",' % py.file()
        self.vscode.launch.sync()


MODULE = meModule()


TITLE = Title('Distilled `metaL` / SICP chapter 4 /')
MODULE['TITLE'] = TITLE

ABOUT = '''
* [`metaL` manifest](https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff)
* SICP:
  * `.html`ed:
    * https://sarabander.github.io/sicp/html/Chapter-4.xhtml
    * http://zv.github.io/sicp-chapter-4
  * in Clojure: http://www.afronski.pl/sicp-in-clojure/2015/10/05/sicp-in-clojure-chapter-4.html
'''
MODULE['ABOUT'] = ABOUT

GITHUB = Url('https://github.com/ponyatov/metaL/tree/master/')
GITHUB['branch'] = ''
MODULE['GITHUB'] = GITHUB

README = README(MODULE)
MODULE.diroot // README
README.sync()

py.top // f'## @brief {TITLE} -- reference implementation'
py.top // ('## ' + Url('https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d').file())


## @name Object
## @{

py.objs = Section('Object')
py.mid // py.objs

## `class Object`
py.obj = pyClass('Object')
py.objs // py.obj

## `class Nil`
py.nil = pyClass('Nil', [py.obj])
py.objs // py.nil

## `class Error`
py.err = Class('Error', [py.obj])
py.objs // py.err

## @name Primitive
## @{

py.prims = Section('Primitive')
py.mid // py.prims

## `class Primitive`
py.prim = Class('Primitive', [py.obj])
py.prims // py.prim

## `class Symbol`
py.sym = Class('Symbol', [py.prim])
py.prims // py.sym

## `class String`
py.str = Class('String', [py.prim])
py.prims // py.str

## `class Number`
py.num = Class('Number', [py.prim])
py.prims // py.num

## `class Integer`
py.int = Class('Integer', [py.prim])
py.prims // py.int

## @}

## @name Container
## @{

py.conts = Section('Container')
py.mid // py.conts

## `class Container`
py.cont = Class('Container', [py.obj])
py.conts // py.cont

## `class Vector`
py.vect = Class('Vector', [py.cont])
py.conts // py.vect

## `class Stack` FIFO buffer
py.stack = Class('Stack', [py.cont])
py.conts // py.stack

## `class Dict` associative array
py.dict = Class('Dict', [py.cont])
py.conts // py.dict

## `class Set` engle-entry container
py.set = Class('Set', [py.cont])
py.conts // py.set

## `class Queue` LIFO thread-safe buffer
py.queue = Class('Queue', [py.cont])
py.conts // py.queue

## @}

## @name Active
## @{

py.actives = Section('Active')
py.mid // py.actives

## `class Active`
py.active = Class('Active', [py.obj])
py.actives // py.active

# index for later patching
ctxi = Section('Context')
py.actives // ctxi

## `class Context` execution context
py.ctx = Class('Context', [py.active])
ctxi // py.ctx

## `class Fn` function
py.fn = Class('Fn', [py.active])
py.actives // py.fn

## `class Op` operator
py.op = Class('Op', [py.active])
py.actives // py.op

## @}

## @name Meta
## @{

py.metas = Section('Meta')
py.mid // py.metas

## `class Meta`
py.meta = Class('Meta', [py.obj])
py.metas // py.meta

## `class Module` software module (compilation module, library)
py.module = Class('Module', [py.meta])
py.metas // py.module

## `class Class`
py.clazz = Class('Class', [py.meta])
py.metas // py.clazz

## class-bound `Method` (encapsulated function)
py.method = Class('Method', [py.meta, py.fn])
py.metas // py.method

## `Fn`/`Method` and `Class`-inheritance arguments
py.args = Class('Args', [py.meta, py.vect])
py.metas // py.args

## @}

## @name IO
## @{

py.ios = Section('IO')
py.mid // py.ios

## `class IO`
py.io = Class('IO', [py.obj])
py.ios // py.io

## `class Dir`
py.dir = Class('Dir', [py.io])
py.ios // py.dir

## `class File`
py.file = Class('File', [py.io])
py.ios // py.file

## @}


## @name metaL manifest fields
## [metaL manifest](https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff)
## @{

fields = pyInterface('fields: metaL manifest')
py.obj // (fields << Url('https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff#70d2d317a4fd4c95904b0a4bf46f2027'))

## object graph node constructor
init = pyMethod('__init__', ['V'])
fields // init
init //\
    (S('## type/class tag') //
        'self.tag  = self.__class__') //\
    (S('## scalar value: object name, string, number,..') //
        'self.val  = V') //\
    (S('## slots = attributes = associative array') //
        'self.slot = {}') //\
    (S('## nested AST = vector = stack = queue') //
        'self.nest = []') //\
    (S('## parent nodes refset') //
        'self.par  = set()') //\
    (S('## unique global storage identifier (*content* fast 32-bit hash)') //
        'self.gid = id(self)') //\
    ''

## @}

## @name dump
## @{

dumpi = pyInterface('dump')
py.obj // (dumpi << Url('https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d#2cd65706a8b843dca6fa8c4ae69920d5'))

## system method dumps any object in a string form
reprr = (pyMethod('__repr__') // Return('self.dump()'))
dumpi // reprr

## method used in `test_metaL.py` dumps wihout `#hash`/`@id`
testt = (pyMethod('test') // Return('self.dump(test=True)'))
dumpi // testt

## @name metaL sample: how to use "exteral" source elements (shared function [a]rguments)
## @{

## dump recursion depth
adepth = Arg('depth')
## prefix default:''
aprefix = Arg('prefix')
## test flag
atest = Arg('test')

## @}

## full text-tree dump
dump = pyMethod('dump')
dumpi // dump
dump.args //\
    Arg("cycle=[]") //\
    Arg(f"{adepth}=0") //\
    Arg(f"{aprefix}=''") //\
    Arg(f"{atest}=False")
dump //\
    f"ret = self.pad({adepth}) + self.head({aprefix}, {atest})" //\
    (S("for i in sorted(self.slot.keys()):") //
        "ret += self.slot[i].dump(cycle, depth+1, prefix=f'{i} = ', test=test)") //\
    'idx = 0' //\
    (S("for j in self.nest:") //
        "ret += j.dump(cycle, depth+1, prefix=f'{idx}: ', test=test)" //
        "idx += 1") //\
    Return('ret')

## short `<T:V>` header only
head = pyMethod('head')
dumpi // head
head.args // f"{aprefix}=''" // f"{atest}=False"
head //\
    f"ret = '%s<%s:%s>' % (prefix, self._tag(), self._val())" //\
    f"if not test: ret += '#%.8x @%x ' % (self.gid, id(self))" //\
    Return('ret')

## padding method
pad = pyMethod('pad')
dumpi // pad
pad.args // adepth
pad //\
    Return(f"'\\n' + '\\t' * {adepth}")

## `.tag`-formatter for dumps
dtag = pyMethod('_tag')
dumpi // (dtag // Return('self.tag.__name__.lower()'))

## `.val`-formatter for dumps
dval = pyMethod('_val')
dumpi // (dval // Return("'%s' % self.val"))


## @}

## @name operator
## @{

operi = pyInterface('operator')
py.obj // operi

## indexing key
key = Arg('key')
## operand `B`
that = Arg('that')

## most operators return `self` : modified object `A`
rself = Return('self')

## `A[key]`
getitem = pyMethod('__getitem__')
operi // getitem
getitem.args // key
getitem //\
    (S("if isinstance(key,str):") //
     Return(f'self.slot[{key}]')) //\
    (S("if isinstance(key,int):") //
     Return(f'self.nest[{key}]')) //\
    'raise TypeError(key)'

## `A // B -> A.push(B)`
floordiv = pyMethod('__floordiv__')
operi // floordiv
floordiv.args // that
floordiv //\
    f'self.nest.append({that})' //\
    rself

## @}

## @name testing
## @{

test_hello = pyTest('hello')
test_hello['for'] = fields
test // "hello = Object('hello')"
test // "world = Object('world')"
test // test_hello
test_hello //\
    "assert hello.test() == '\\n<object:hello>'" //\
    "assert world.test() == '\\n<object:world>'" //\
    "hello // world" //\
    "print(hello.test())" //\
    (S("assert hello.test() ==\\") //
        "'\\n<object:hello>' +\\" //
        "'\\n\\t0: <object:world>'") //\
    ''

## @}

## @name evaluation
## @{

evali = pyInterface('evaluation')
py.obj // evali

## computation context
ctx = Arg('ctx')

## `.eval()` method template
evall = pyMethod('eval')
evall.args // ctx

## `.apply()` method template
apply = pyMethod('apply')
apply.args // that // ctx

## `Object.eval()`
evali // (evall.cp() // 'raise NotImplementedError')

## `Object.apply()`
evali // (apply.cp() // 'raise NotImplementedError')

# most primitives evaluates to itself
py.prim // (evall.cp() // Return('self'))

# symbol must lookup itself in context
py.sym // (evall.cp() // Return(f'{ctx}[self.val]'))

# for other class evaluation we need to define the global context
ctxi // '' // "glob = Context('global')" // ''

## @}

py.sync()
test.sync()

## @}

# hello = Object('hello')
# hello['world'] = Object('world')
# # hello.world = Object('WORLD')
# print(1,hello)
# print(2,hello.world)
# print(3,hello.val)
# print(4,hello.vaz)
