## @file
## @brief powered by `metaL`

## @defgroup info metainfo
## @{
MODULE = 'metaL'
TITLE = '[meta]programming [L]anguage'
ABOUT = 'homoiconic metaprogramming system\n* powered by `metaL`'
AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = 2020
LICENSE = 'MIT'
GITHUB = 'https://github.com/ponyatov'
LOGO = 'logo.png'
## @}

import os, sys, random

## @defgroup persist Persistence
## @brief inherit `Unison` *immutable global storage*: https://www.unisonweb.org

import xxhash

## @defgroup object Object

## @brief base object graph node
## @ingroup object
class Object:

    ## construct object
    ## @param[in] V given scalar value
    def __init__(self, V):
        if isinstance(V, Object):
            V = V.val
        ## name / scalar value
        self.val = V
        ## attributes = dict = env
        self.slot = {}
        ## nested AST = vector = stack = queue
        self.nest = []
        ## global storage id
        ## @ingroup persist
        self.gid = self.sync().gid

    ## @name storage/hot-update
    ## @{

    ## this method must be called on any object update
    ## (compute hash, update persistent memory,..)
    ##
    ## mostly used in operator methods in form of `return self.sync()`
    ## @ingroup persist
    ## @returns self
    def sync(self):
        # update global hash
        self.gid = hash(self)
        ## sync with storage
        #storage.put(self)
        return self

    ## fast object hashing for global storage id
    ## @ingroup persist
    def __hash__(self):
        hsh = xxhash.xxh32()
        hsh.update(self._type())
        hsh.update('%s' % self.val)
        for i in self.slot:
            hsh.update(i)
            hsh.update(self.slot[i].gid.to_bytes(8, 'little'))
        for j in self.nest:
            hsh.update(j.gid.to_bytes(8, 'little'))
        return hsh.intdigest()

    ## serialize to .json
    ## @ingroup persist
    def json(self):
        js = '{"gid":"%x","type":"%s","val":"%s",' % (
            self.gid, self._type(), self.val)
        slots = []
        for k in sorted(self.slot.keys()):
            slots.append('"%s":"%.8x"' % (k, self.slot[k].gid))
        js += '"slot":{%s},' % ','.join(slots)
        nested = []
        for i in self.nest:
            nest.append('"%.8x"' % i.gid)
        js += '"nest":[%s]' % ','.join(nested)
        return js + "}"

    ## @}

    ## @name dump
    ## @{

    ## `print` callback
    def __repr__(self): return self.dump()

    ## dump for tests (no hash/gid in headers)
    def test(self): return self.dump(test=True)

    ## dump in full text tree form
    ## @param[in] cycle already dumped objects (cycle prevention registry)
    ## @param[in] depth recursion depth
    ## @param[in] prefix optional prefix in `<T:V>` header
    ## @param[in] test test dump option @ref test
    def dump(self, cycle=None, depth=0, prefix='', test=False):
        # header
        tree = self._pad(depth) + self.head(prefix, test)
        # cycles
        if not depth:
            cycle = []
        if self in cycle:
            return tree + ' _/'
        else:
            cycle.append(self)
        # slot{}s
        for k in sorted(self.slot.keys()):
            tree += self.slot[k].dump(cycle, depth + 1, '%s = ' % k, test)
        # nest[]ed
        for i, j in enumerate(self.nest):
            tree += j.dump(cycle, depth + 1, '%s: ' % i, test)
        # subtree
        return tree

    ## paddig for @ref dump
    def _pad(self, depth): return '\n' + '\t' * depth

    ## short `<T:V>` header only
    ## @param[in] prefix optional prefix in `<T:V>` header
    ## @param[in] test test dump option @ref test
    def head(self, prefix='', test=False):
        hdr = '%s<%s:%s>' % (prefix, self._type(), self._val())
        if not test:
            hdr += ' #%.8x @%x' % (self.gid, id(self))
        return hdr

    ## object class name (lowercased as marker of instance)
    def _type(self): return self.__class__.__name__.lower()

    ## `.val` output for dumps (limited length, escaped control chars)
    def _val(self): return '%s' % self.val

    ## @}

    ## @name operator
    ## @{

    ## `A[key] ~> A.slot[key:str] | A.nest[key:int] `
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nest[key]
        if isinstance(key, str):
            return self.slot[key]
        raise TypeError(key)

    ## `A[key] = B`
    def __setitem__(self, key, that):
        assert isinstance(key, str)
        if isinstance(that, str):
            that = String(that)
        if isinstance(that, int):
            that = Integer(that)
        self.slot[key] = that
        return self.sync()

    ## `A << B ~> A[B.type] = B`
    def __lshift__(self, that):
        return self.__setitem__(that._type(), that)

    ## `A >> B ~> A[B.val] = B`
    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    ## `A // B -> A.push(B)`
    ## @param[in] that `B`
    ## @param[in] sync add object with sync
    ## (hash/storage update, use `False` for massive & IO pushes)
    def __floordiv__(self, that, sync=True):
        if isinstance(that, str):
            that = String(that)
        self.nest.append(that)
        if sync:
            return self.sync()
        return self

    ## @}

    ## @name evaluation
    ## @{

    ## evaluate in context
    ## @param[in] ctx context

    def eval(self, ctx): raise Error((self))

    ## apply as function
    ## @param[in] that operand (function argument/s)
    ## @param[in] ctx context
    def apply(self, that, ctx): raise Error((self))

    ## @}

    ## @name code generation
    ## @{

    ## to generic text file: use `.json` in place of `Error`
    ## @ingroup gen
    def file(self, comment=None): return self.json()

    ## to Python code: use `.json` in place of `Error`
    ## @ingroup py
    def py(self): return self.json()

    ## @}


## @defgroup error Error
## @ingroup object

## @ingroup error
class Error(Object, BaseException):
    pass


## @defgroup prim Primitive
## @ingroup object

## @ingroup prim
class Primitive(Object):
    ## primitives evaluates to itself
    def eval(self, ctx): return self

## @ingroup prim
class Symbol(Primitive):
    ## symbol evaluates via context lookup
    def eval(self, ctx): return ctx[self.val]

## @ingroup prim
class String(Primitive):
    def _val(self):
        s = ''
        for c in self.val:
            if c == '\n':
                s += r'\n'
            elif c == '\r':
                s += r'\r'
            elif c == '\t':
                s += r'\t'
            else:
                s += c
        return s

    def file(self): return self.val

## @ingroup prim
## floating point
class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

    ## @name operator
    ## @{

    ## `+A`
    def plus(self, ctx):
        return self.__class__(+self.val)

    ## `-A`
    def minus(self, ctx):
        return self.__class__(-self.val)

    ## `A + B`
    def add(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val + that.val)

    ## `A - B`
    def sub(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val - that.val)

    ## `A * B`
    def mul(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val * that.val)

    ## `A / B`
    def div(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val / that.val)

    ## `A ^ B`
    def pow(self, that, ctx):
        assert type(self) == type(that)
        return self.__class__(self.val ** that.val)

    ## @}

## @ingroup prim
class Integer(Number):
    def __init__(self, V):
        Primitive.__init__(self, int(V))

## @ingroup prim
## hexadecimal machine number
class Hex(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x10))

    def _val(self):
        return hex(self.val)

## @ingroup prim
## bit string
class Bin(Integer):
    def __init__(self, V):
        Primitive.__init__(self, int(V[2:], 0x02))

    def _val(self):
        return bin(self.val)

## @defgroup cont Container
## @ingroup object

## @ingroup cont
## generic data container
class Container(Object):
    pass

## @ingroup cont
## var size array (Python list)
class Vector(Container):
    def eval(self, ctx):
        res = self.__class__(self.val)
        for i in self.nest:
            res // i.eval(ctx)
        return res

## @ingroup cont
## FIFO stack
class Stack(Container):
    pass

## @ingroup cont
## associative array
class Dict(Container):
    pass


## @defgroup active Active
## @ingroup object

## @ingroup active
## executable data elements
class Active(Object):
    pass

## @ingroup active
## function
class Fn(Active):
    pass

## @ingroup active
## operator
class Op(Active):
    def eval(self, ctx):
        # greedy computation for all subtrees
        greedy = list(map(lambda i: i.eval(ctx), self.nest))
        # unary
        if len(greedy) == 1:
            if self.val == '+':
                return greedy[0].plus(ctx)
            if self.val == '-':
                return greedy[0].minus(ctx)
        # binary
        if len(greedy) == 2:
            if self.val == '+':
                return greedy[0].add(greedy[1], ctx)
            if self.val == '-':
                return greedy[0].sub(greedy[1], ctx)
            if self.val == '*':
                return greedy[0].mul(greedy[1], ctx)
            if self.val == '/':
                return greedy[0].div(greedy[1], ctx)
            if self.val == '^':
                return greedy[0].pow(greedy[1], ctx)
        # unknown
        raise Error((self))

## @ingroup active
## Virtual Machine (environment + stack + message queue)
class VM(Active):
    pass


## @ingroup active
## global system VM
vm = VM(MODULE)
vm << vm


## @defgroup meta Meta
## @ingroup object

## @ingroup meta
class Meta(Object):
    pass

## @ingroup meta
class Module(Meta):
    pass

## @ingroup meta
class Section(Meta):
    def file(self, comment='#'):
        ret = '%s \\ %s\n\n' % (comment, self.head(test=True))
        for i in self.nest:
            ret += i.file() + '\n'
        ret += '\n%s / %s\n\n' % (comment, self.head(test=True))
        return ret


## @defgroup io IO
## @ingroup object
## @brief base file output

## @ingroup io
class IO(Object):
    pass

## @ingroup io
class Dir(IO):
    def __init__(self, V):
        IO.__init__(self, V)
        try:
            os.mkdir(self.val)
        except FileExistsError:
            pass

    ## append file
    def __floordiv__(self, that):
        assert isinstance(that, File)
        that.fh = open('%s/%s' % (self.val, that.val), 'w')
        return IO.__floordiv__(self, that)


## @ingroup io
class File(IO):
    def __init__(self, V, comment='#'):
        self.fh = None
        self.comment = comment
        IO.__init__(self, V)

    def sync(self):
        if self.fh:
            self.fh.seek(0)
            for i in self.nest:
                self.fh.write(i.file() + '\n')
            self.fh.flush()
        return IO.sync(self)

    ## push object/line
    ## @param[in] sync `=False` default w/o flush to disk (via `sync()``)
    def __floordiv__(self, that, sync=False):
        return IO.__floordiv__(self, that, sync)

## @defgroup net Networking
## @ingroup io
## networking object
class Net(IO):
    pass

## @ingroup net
## TCP/IP address
class Ip(Net):
    pass

## @ingroup net
## TCP/IP port
class Port(Net):
    pass

## @ingroup net
class Email(Net):
    pass

## @ingroup net
class Url(Net):
    pass

## @ingroup net
class User(Net):
    pass

## @ingroup net
## password
class Pswd(Net):
    def __init__(self, V):
        Net.__init__(self, V, minsize=6)
        self.minsize = minsize

    def _val(self): return '*' * self.minsize

## @defgroup doc Documenting

## @ingroup doc
class Doc(Object):
    pass

## @ingroup doc
class Title(Doc):
    pass

## @ingroup doc
class Author(Doc):
    pass

## @ingroup doc
class License(Doc):
    pass


## @ingroup info
## @{
vm['MODULE'] = MODULE = Module(MODULE)
vm['TITLE'] = TITLE = Title(TITLE)
vm['ABOUT'] = ABOUT = String(ABOUT)
vm['EMAIL'] = EMAIL = Email(EMAIL)
vm['AUTHOR'] = AUTHOR = Author(AUTHOR) << EMAIL
vm['YEAR'] = YEAR = Integer(YEAR)
vm['LICENSE'] = LICENSE = License(LICENSE)
vm['GITHUB'] = GITHUB = Url(GITHUB)
vm['LOGO'] = LOGO = File(LOGO)
## @}


## @defgroup gen CodeGen
## @brief Code generators

## @ingroup gen
class gitIgnore(File):
    def __init__(self, V='.gitignore'):
        File.__init__(self, V)
        self // '*~\n*.swp'
        self // ''
        self // '*.log\n*.exe\n*.o'

## @defgroup mk Makefile
## @ingroup gen

## @ingroup mk
class Makefile(File):
    def __init__(self, V='Makefile'):
        File.__init__(self, V, comment='#')
        h = Section('head')
        h // 'CWD     = $(CURDIR)'
        h // 'MODULE  = $(notdir $(CWD))'
        h // 'OS     ?= $(shell uname -s)'
        h // ''
        h // 'NOW = $(shell date +%d%m%y)'
        h // 'REL = $(shell git rev-parse --short=4 HEAD)'
        self >> h
        t = Section('tail')
        t // '.PHONY: install update'
        t // 'install:\n\t$(MAKE) $(OS)_install'
        t // 'update:\n\t$(MAKE) $(OS)_update'
        t // '\n.PHONY: Linux_install Linux_update'
        t // '\nLinux_install Linux_update:'
        t // '\tsudo apt update'
        t // '\tsudo apt install -u `cat apt.txt`'
        self >> t

    def sync(self):
        if self.fh:
            self.fh.seek(0)
            self.fh.write(self['head'].file(self.comment))
            for i in self.nest:
                self.fh.write(i.file() + '\n')
            self.fh.write(self['tail'].file(self.comment))
            self.fh.flush()
        return IO.sync(self)

## @defgroup cc C99
## @ingroup gen

## @ingroup py
class cFile(File):
    def __init__(self, V, comment='//'):
        File.__init__(self, V, comment)

## @defgroup py Python
## @ingroup gen

## @ingroup py
class pyMakefile(Makefile):
    def __init__(self, V='Makefile'):
        Makefile.__init__(self, V)
        h = Section('python tools')
        self['head'] // h
        h // 'PIP = $(CWD)/bin/pip3'
        h // 'PY  = $(CWD)/bin/python3'
        h // 'PYT = $(CWD)/bin/pytest'
        h // 'PEP = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402'


## @ingroup py
class pygIgnore(gitIgnore):
    def __init__(self, V='.gitignore'):
        gitIgnore.__init__(self, V)
        self // '''
*.pyc
/bin/
/include/
/lib/
/lib64/
/share/
pyvenv.cfg
config.py'''


## @defgroup lexer lexer
## @ingroup parser

import ply.lex as lex

## @ingroup lexer
## token types
tokens = ['symbol',
          'number', 'integer', 'hex', 'bin',
          'lp', 'rp', 'lq', 'rq', 'lc', 'rc',
          'add', 'sub', 'mul', 'div', 'pow',
          'comma',
          'exit']

## @ingroup lexer
## drop spaces
t_ignore = ' \t\r'

## @ingroup lexer
## line commens starts with `#`
t_ignore_comment = r'\#.*'

## @ingroup lexer
## increment line counter on every new line
def t_nl(t):
    r'\n'
    t.lexer.lineno += 1

## @ingroup lexer
## process `exit()` as special CLI command
def t_exit(t):
    r'exit\(\)'
    return t

## @name paren
## @{

## @ingroup lexer
## `(`
def t_lp(t):
    r'\('
    return t
## @ingroup lexer
## `)`
def t_rp(t):
    r'\)'
    return t
## @ingroup lexer
## `[`
def t_lq(t):
    r'\['
    return t
## @ingroup lexer
## `]`
def t_rq(t):
    r'\]'
    return t
## @ingroup lexer
## `{`
def t_lc(t):
    r'\{'
    return t
## @ingroup lexer
## `}`
def t_rc(t):
    r'\}'
    return t

## @}

## @name delimiter
## @{

## @ingroup lexer
## `,` split vector elements
def t_comma(t):
    r','
    return t

## @}

## @name operator
## @{

## @ingroup lexer
## `+`
def t_add(t):
    r'\+'
    t.value = Op(t.value)
    return t
## @ingroup lexer
## `-`
def t_sub(t):
    r'\-'
    t.value = Op(t.value)
    return t
## @ingroup lexer
## `*`
def t_mul(t):
    r'\*'
    t.value = Op(t.value)
    return t
## @ingroup lexer
## `/`
def t_div(t):
    r'\/'
    t.value = Op(t.value)
    return t
## @ingroup lexer
## `^`
def t_pow(t):
    r'\^'
    t.value = Op(t.value)
    return t

## @}

## @name lexeme
## @{

## @ingroup lexer
##    r`[0-9]+\.[0-9]*([eE][+\-]?[0-9]+)?`
def t_number(t):
    r'[0-9]+\.[0-9]*([eE][+\-]?[0-9]+)?'
    t.value = Number(t.value)
    t.type = 'number'
    return t

## @ingroup lexer
##    r`[0-9]+[eE][+\-]?[0-9]+`
def t_number_exp(t):
    r'[0-9]+[eE][+\-]?[0-9]+'
    t.value = Number(t.value)
    t.type = 'number'
    return t

## @ingroup lexer
##    r`0x[0-9a-fA-F]+`
def t_hex(t):
    r'0x[0-9a-fA-F]+'
    t.value = Hex(t.value)
    return t

## @ingroup lexer
##    r`0b[01]+`
def t_bin(t):
    r'0b[01]+'
    t.value = Bin(t.value)
    return t

## @ingroup lexer
##    r`[0-9]+`
def t_integer(t):
    r'[0-9]+'
    t.value = Integer(t.value)
    return t

## @ingroup lexer
##    r`[^ \t\r\n\#\+\-\*\/\^]+`
def t_symbol(t):
    r'[^ \t\r\n\#\+\-\*\/\^\\(\)\[\]\{\}]+'
    t.value = Symbol(t.value)
    return t

## @}

## @ingroup lexer
## lexer error callback
def t_ANY_error(t): raise SyntaxError(t)


## @ingroup lexer
## PLY lexer
lexer = lex.lex()

## @defgroup parser parser
## @brief `optional` syntax parser for CLI DML/DDL

import ply.yacc as yacc

## @ingroup parser
## Abstract Syntax Tree =~= any `metaL` graph
class AST(Vector):
    pass

## @ingroup parser
##    ' REPL : '
## create empty AST on recursion start
def p_REPL_none(p):
    ' REPL : '
    p[0] = AST('')

## @ingroup parser
##    ' REPL : REPL ex '
## collect every parsed [ex]pression
def p_REPL_recursion(p):
    ' REPL : REPL ex '
    p[0] = p[1] // p[2]

## @ingroup parser
##    ' REPL : exit '
## process `exit()` as special CLI command
def p_REPL_exit(p):
    ' REPL : exit '
    p[0] = None

## @name operator
## @{


## @ingroup parser
precedence = (
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div'),
    ('left', 'pow', ),
    ('left', 'pfx', ),
)

## @ingroup parser
##    ' ex : add ex %prec pfx ' `+A`
def p_ex_plus(p):
    ' ex : add ex %prec pfx '
    p[0] = p[1] // p[2]
## @ingroup parser
##    ' ex : sub ex %prec pfx ' `-A`
def p_ex_minus(p):
    ' ex : sub ex %prec pfx '
    p[0] = p[1] // p[2]

## @ingroup parser
##    ' ex : ex add ex '
def p_ex_add(p):
    ' ex : ex add ex '
    p[0] = p[2] // p[1] // p[3]
## @ingroup parser
##    ' ex : ex sub ex '
def p_ex_sub(p):
    ' ex : ex sub ex '
    p[0] = p[2] // p[1] // p[3]
## @ingroup parser
##    ' ex : ex mul ex '
def p_ex_mul(p):
    ' ex : ex mul ex '
    p[0] = p[2] // p[1] // p[3]
## @ingroup parser
##    ' ex : ex div ex '
def p_ex_div(p):
    ' ex : ex div ex '
    p[0] = p[2] // p[1] // p[3]
## @ingroup parser
##    ' ex : ex pow ex '
def p_ex_pow(p):
    ' ex : ex pow ex '
    p[0] = p[2] // p[1] // p[3]

## @}

## @name parens
## @{

## @ingroup parser
def p_ex_parens(p):
    ' ex : lp ex rp '
    p[0] = p[2]

## @ingroup parser
def p_ex_curles(p):
    ' ex : lc ex rc '
    p[0] = Fn('') // p[2]

## @}

## @name vector
## @{

## @ingroup parser
def p_ex_vector(p):
    ' ex : lq vector rq '
    p[0] = p[2]
## @ingroup parser
def p_vector_empty(p):
    ' vector : '
    p[0] = Vector('')
## @ingroup parser
def p_vector_single(p):
    ' vector : vector ex '
    p[0] = p[1] // p[2]
## @ingroup parser
def p_vector_many(p):
    ' vector : vector comma ex '
    p[0] = p[1] // p[3]

## @}

## @name number
## @{

## @ingroup parser
##    r' ex : number '
def p_ex_number(p):
    r' ex : number '
    p[0] = p[1]
## @ingroup parser
##    r' ex : integer '
def p_ex_integer(p):
    r' ex : integer '
    p[0] = p[1]
## @ingroup parser
##    r' ex : hex '
def p_ex_hex(p):
    r' ex : hex '
    p[0] = p[1]
## @ingroup parser
##    r' ex : bin '
def p_ex_bin(p):
    r' ex : bin '
    p[0] = p[1]

## @}

## @ingroup parser
##    ' ex : symbol '
def p_ex_symbol(p):
    ' ex : symbol '
    p[0] = p[1]

## @ingroup parser
## syntax error callback
def p_error(p): raise SyntaxError(p)


## @ingroup parser
## PLY parser
parser = yacc.yacc(debug=False, write_tables=False)


## @defgroup repl REPL
## @ingroup parser
## @brief Read-Eval-Print-Loop: interactive command line

## @ingroup repl
## process command/script (in optional DDL/DML syntax)
## @param[in] src source code string
## @exception TypeError on `"exit()"` in CLI
## (to be compatible with Python interactive session & VSCode)
def metaL(src):
    import traceback
    for ast in parser.parse(src):
        print(ast)
        try:
            print(ast.eval(vm))
            print(vm)
        except Exception as e:
            traceback.print_exc()
        print('-' * 66)

## @ingroup repl
## Read-Eval-Print-Loop in Python: input single line from user, and run parser (interpreter)
def REPL():
    print(vm)
    while True:
        command = input(vm.head(test=True) + ' ')
        try:
            metaL(command)
        except TypeError: # executes on `exit()` in REPL input
            os._exit(0)

## @defgroup init system init

## @ingroup init
## handle command-line arguments as filenames must be interpreted
def init():
    for init in sys.argv[1:]:
        with open(init) as src:
            metaL(src.read())


if __name__ == '__main__':
    init()
    REPL()
