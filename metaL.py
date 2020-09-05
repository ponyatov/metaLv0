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
        ## symbol name / scalar value (string, number,..)
        self.val = V
        ## slots = attributes = dict = env
        self.slot = {}
        ## nested AST = vector = stack = queue
        self.nest = []
        ## parent nodes registry
        self.par = set()
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
            nested.append('"%.8x"' % i.gid)
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

    ## @name plot
    ## @{

    ## plot object graph via GraphViz/`dot`
    ## @returns `digraph{}` string for `dot`
    ## @param[in] cycle block (plottted nodes accumulator list
    ## @param[in] depth recursion depth
    ## @param[in] parent node
    ## @param[in] label on edge
    ## @param[in] color of edge
    def plot(self, cycle=None, depth=0, parent=None, label='', color='black'):
        # recursion root
        if not depth:
            dig = 'digraph "%s" {\nrankdir=LR;\n' % self.head(test=True)
            cycle = []
        else:
            dig = '\t' * depth
        # node
        me = 'zid%s' % id(self)
        dig += '%s [label="%s"]\n' % (me, self.head(test=True))
        # edge
        if parent:
            dig += '\t' * depth + \
                '%s -> %s [label="%s",color="%s"]\n' % (
                    parent, me, label, color)
        # cycles block
        if self in cycle:
            return dig
        else:
            cycle += [self]
        # slots
        for i in sorted(self.slot.keys()):
            dig += self.slot[i].plot(cycle, depth + 1,
                                     parent=me, label=i, color='blue')
        # recursion root
        if not depth:
            dig += '}\n'
            with open('/tmp/dot.dot', 'w') as f:
                f.write(dig)
            return dig
        else:
            return dig

    ## @}

    ## @name operator
    ## @{

    ## `A.keys()`
    def keys(self):
        return self.slot.keys()

    ## `A[key] ~> A.slot[key:str] | A.nest[key:int] `
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.nest[key]
        if isinstance(key, str):
            try:
                return self.slot[key]
            except KeyError:
                return Undef(key) // self
        raise TypeError(key)

    ## `A.B`
    def dot(self, that, ctx):
        assert isinstance(that, Object)
        return self[that.val]

    ## `A[key] = B`
    def __setitem__(self, key, that):
        if isinstance(that, str):
            that = String(that)
        if isinstance(that, int):
            that = Integer(that)
        if isinstance(key, str):
            self.slot[key] = that
        elif isinstance(key, int):
            self.nest[key] = that
        else:
            raise TypeError(key)
        return self.sync()

    ## `A << B ~> A[B.type] = B`
    def __lshift__(self, that):
        if isinstance(that, str):
            that = String(that)
        return self.__setitem__(that._type(), that)

    ## `A >> B ~> A[B.val] = B`
    def __rshift__(self, that):
        return self.__setitem__(that.val, that)

    ## `A // B -> A.push(B)`
    ## @param[in] that `B`
    ## @param[in] sync push object with sync
    ## (hash/storage update, use `False` for massive & IO pushes)
    def __floordiv__(self, that, sync=True):
        return self.push(that, sync)

    ## @}

    ## @name stack ops
    ## @{

    ## clean `.nest[]`
    def dropall(self): self.nest = []

    ## push to `.nest[]`
    ## @param[in] sync push with sync
    ## @param[in] that `B` operand to be pushed
    def push(self, that, sync=True):
        if isinstance(that, str):
            that = String(that)
        self.nest.append(that)
        that.par.add(self)
        if sync:
            return self.sync()
        return self

    ## insert `that` into parent node after the current
    def after(self, that):
        assert len(self.par) == 1
        for parent in self.par:
            index = parent.index(self)
            parent.insert(index+1,that)
        return self

    ## insert `A[index]=B`
    ## @param[in] index integer indsex in `.nest[]`
    ## @param[in] that `B` operand to be inserted
    def insert(self,index,that):
        self.nest.insert(index,that)
        return self

    def drop(self): self.nest.pop(); return self

    ## find index of subgraph
    def index(self, that):
        return self.nest.index(that)

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

## @ingroup error
class Undef(Object):
    pass

## @defgroup prim Primitive
## @ingroup object

## @ingroup prim
class Primitive(Object):
    ## primitives evaluates to itself
    def eval(self, ctx): return self

## @ingroup Nil
class Nil(Primitive):
    def __init__(self): Primitive.__init__(self, '')

## @ingroup prim
class Symbol(Primitive):

    ## symbol evaluates via context lookup
    def eval(self, ctx): return ctx[self.val]

    ## assignment
    def eq(self, that, ctx):
        ctx[self.val] = that
        return that

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

    def py(self): return self.val

    def cc_arg(self): return '"%s"' % self._val()

## @ingroup prim
## floating point
class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

    def file(self): return '%s' % self.val

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
    def __init__(self, V=''):
        super().__init__(V)

    def eval(self, ctx):
        res = self.__class__(self.val)
        for i in self.nest:
            res // i.eval(ctx)
        return res

    def cc_arg(self):
        ret = ','.join([j.cc_arg() for j in self.nest])
        return '/* %s */ %s' % (self.head(), ret)

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
    def eval(self, ctx): return self

    def apply(self, that, ctx):
        self['arg'] = that
        self['ret'] = Nil()
        print('self', self)
        print('that', that)
        return self['ret']

    def at(self, that, ctx): return self.apply(that, ctx)

## @ingroup active
## operator
class Op(Active):
    def eval(self, ctx):
        if self.val == '`':
            return self.nest[0]
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
            if self.val == '=':
                return greedy[0].eq(greedy[1], ctx)
            if self.val == '.':
                return greedy[0].dot(greedy[1], ctx)
            if self.val == ':':
                return greedy[0].colon(greedy[1], ctx)
            if self.val == '@':
                return greedy[0].at(greedy[1], ctx)
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
class Class(Meta):
    def __init__(self, C):
        assert type(C) == type(Class)
        Meta.__init__(self, C.__name__)
        self.C = C

    def colon(self, that, ctx):
        return self.C(that)

    def py(self):
        return 'class %s: pass' % self.val

## @ingroup meta
class Module(Meta):
    def file(self): return self.head(test=True)


vm['module'] = Class(Module)

## @ingroup meta
class Section(Meta):
    def __init__(self, V, comment='#'):
        self.comment = comment
        Meta.__init__(self, V)

    def file(self):
        ret = ''
        if self.comment:
            ret += '\n%s \\ %s' % (self.comment, self.head(test=True))
        for i in self.nest:
            ret += '\n%s' % i.file()
        if self.comment:
            ret += '\n%s / %s' % (self.comment, self.head(test=True))
        return ret

    def py(self): return self.file()

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

    def sync(self):
        try:
            os.mkdir(self.val)
        except FileExistsError:
            pass
        return IO.sync(self)

    ## append file
    def __floordiv__(self, that):
        if isinstance(that, File):
            that.fh = open('%s/%s' % (self.val, that.val), 'w')
            return IO.__floordiv__(self, that)
        if isinstance(that, Dir):
            that.val = '%s/%s' % (self.val, that.val)
            return IO.__floordiv__(self, that)
        raise Error((self))


## @ingroup io
class File(IO):
    def __init__(self, V, ext='', comment='#'):
        self.fh = None
        self.comment = comment
        super().__init__(V)
        self.ext = ext
        self.top = self['top'] = Section('top', comment)
        self.mid = self['mid'] = Section('mid', comment)
        self.bot = self['bot'] = Section('bot', comment)
        if self.comment:
            powered = "powered by metaL: https://repl.it/@metaLmasters/metaL#README.md"
            if len(self.comment) == len('#'):
                self.top // ("%s  %s" % (self.comment, powered))
                self.top // ("%s%s @file" % (self.comment, self.comment,))
            elif len(self.comment) == len('//'):
                self.top // ("%s %s" % (self.comment, powered))
                self.top // ("%s @file" % self.comment)
            else:
                raise Error((self.comment))

    def file(self): return '%s%s' % (self.val, self.ext)

    def sync(self):
        if self.fh:
            self.fh.seek(0)
            self.fh.write(self.top.file())
            self.fh.write(self.mid.file())
            for j in self.nest:
                self.fh.write(j.file() + '\n')
            self.fh.write(self.bot.file())
            self.fh.truncate()
            self.fh.flush()
        return super().sync()

    ## push object/line
    ## @param[in] that `B` operand: string of section will be pushed into file
    ## @param[in] sync `=False` default w/o flush to disk (via `sync()``)
    def __floordiv__(self, that, sync=False):
        return super().__floordiv__(that, sync)

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
    def file(self): return '<%s>' % self.val

## @ingroup net
class Url(Net):
    def file(self): return self.val

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
    def file(self): return '%s' % self.val

## @ingroup doc
class Title(Doc):
    ## @ingroup py
    def py(self): return '## @brief %s' % self.val

## @ingroup doc
class Author(Doc):
    pass


from license import License, MIT

## @ingroup info
## @{
vm['MODULE'] = MODULE = Module(MODULE)
vm['TITLE'] = TITLE = Title(TITLE)
vm['ABOUT'] = ABOUT = String(ABOUT)
vm['EMAIL'] = EMAIL = Email(EMAIL)
vm['AUTHOR'] = AUTHOR = Author(AUTHOR) << EMAIL
vm['YEAR'] = YEAR = Integer(YEAR)
vm['LICENSE'] = LICENSE = MIT
vm['GITHUB'] = GITHUB = Url(GITHUB)
vm['LOGO'] = LOGO = File(LOGO)
## @}


## @defgroup gen CodeGen
## @brief Code generators

## @defgroup prj Project
## @ingroup gen
## @brief generic software project components

## @ingroup prj
class README(File):
    def __init__(self, module):
        File.__init__(self, 'README.md', comment=None)
        self.module = module
        self // ('#  `%s`' % module.val)
        self // ('## %s' % module['TITLE'].val)
        # self // ''
        about = module['ABOUT'].val
        while about[-1] in '\r\n':
            about = about[:-1]
        about += '\n* powered by `metaL`'
        self // ('%s' % about)
        self // ''
        self // ('(c) %s <<%s>> %s %s' % (
            module['AUTHOR'].val, module['EMAIL'].val,
            module['YEAR'].val, module['LICENSE'].val))
        self.github = Section('github', comment=None)
        self // self.github
        self.github // ('github: %s%s%s' %
                        (module['GITHUB'].val, module.val, module['GITHUB']['branch'].val))


## @ingroup prj
class Makefile(File):
    def __init__(self, V='Makefile'):
        super().__init__(V, comment='#')

## @ingroup prj
## system setting
class Setting(Meta):
    def __init__(self, key, val):
        Meta.__init__(self, key)
        self.key = key
        self // val

    def __floordiv__(self, that):
        self.nest = []
        Meta.__floordiv__(self, that)

## @ingroup prj
## VSCode multicommand
class multiCommand(Setting):
    def __init__(self, key, val):
        Setting.__init__(self, key, val)

    def file(self):
        ret = '\t{'
        ret += '"command":"multiCommand.%s",' % self.key
        ret += '"sequence":['
        ret += '\n\t\t"workbench.action.files.saveAll",'
        ret += '\n\t\t{"command": "workbench.action.terminal.sendSequence",'
        ret += '\n\t\t "args": {"text": "\\u000D%s\\u000D"}}' % self.nest[0].val
        ret += '\n\t],},'
        return ret

## @ingroup prj
## module with its own directory (root module = project)
class dirModule(Module):
    def __init__(self, V=None):
        if not V:
            V = __import__('sys').argv[0]
            V = V.split('/')[-1]
            V = V.split('.')[0]
        super().__init__(V)
        self['AUTHOR'] = self.AUTHOR = vm['AUTHOR']
        self['EMAIL'] = self.EMAIL = vm['EMAIL']
        self['YEAR'] = self.YEAR = vm['YEAR']
        self['LICENSE'] = vm['LICENSE']
        # diroot
        self['dir'] = self.diroot = Dir(V)
        # Makefile
        self.init_mk()
        # apt.txt
        self.init_apt()
        # gitignore
        self.init_giti()

    def init_mk(self):
        self.diroot['mk'] = self.mk = Makefile()
        self['mk'] = self.mk
        self.diroot // self.mk
        # vars
        self.mk['vars'] = self.mk.vars = Section('vars')
        self.mk.top // self.mk.vars
        self.mk.vars // f'{"MODULE":<8} = $(notdir $(CURDIR))'
        self.mk.vars // f'{"OS":<7} ?= $(shell uname -s)'
        # version
        self.mk['version'] = self.mk.version = Section('version')
        self.mk.top // self.mk.version
        self.mk.version // f'{"NOW":<8} = $(shell date +%d%m%y)'
        self.mk.version // f'{"REL":<8} = $(shell git rev-parse --short=4 HEAD)'
        # dirs
        self.mk['dirs'] = self.mk.dirs = Section('dirs')
        self.mk.top // self.mk.dirs
        self.mk.dirs // f'{"CWD":<8} = $(CURDIR)'
        self.mk.dirs // f'{"TMP":<8} = $(CWD)/tmp'
        self.mk.dirs // f'{"SOURCE":<8} = $(TMP)/src'
        # tools
        self.mk['tools'] = self.mk.tools = Section('tools')
        self.mk.top // self.mk.tools
        self.mk.tools // f'{"WGET":<8} = wget -c --no-check-certificate'
        self.mk.tools // f'{"CORES":<8} = $(shell grep proc /proc/cpuinfo|wc -l)'
        self.mk.tools // f'{"XMAKE":<8} = $(XPATH) $(MAKE) -j$(CORES)'
        # install/update
        self.mk['install'] = self.mk.install = Section('install')
        self.mk.bot // self.mk.install
        self.mk.install // '.PHONY: install'
        self.mk.install // 'install:\n\t$(MAKE) $(OS)_install'
        self.mk['update'] = self.mk.update = Section('update')
        self.mk.bot // self.mk.update
        self.mk.update // '.PHONY: update'
        self.mk.update // 'update:\n\t$(MAKE) $(OS)_update'
        self.mk['linux'] = self.mk.linux = Section('linux/install')
        self.mk.bot // self.mk.linux
        self.mk.linux // '.PHONY: Linux_install Linux_update'
        self.mk.linux // 'Linux_install Linux_update:'
        self.mk.linux // '\tsudo apt update'
        self.mk.linux // '\tsudo apt install -u `cat apt.txt`\n'
        # merge master/shadow
        self.mk['merge'] = self.mk.merge = Section('merge')
        self.mk.bot // self.mk.merge
        self.mk.merge // 'MERGE  = Makefile apt.txt .gitignore'
        self.mk.merge // 'MERGE += README.md'
        # master
        self.mk.bot // 'master:'
        self.mk.bot // '\tgit checkout $@'
        self.mk.bot // '\tgit pull -v'
        self.mk.bot // '\tgit checkout shadow -- $(MERGE)'
        # shadow
        self.mk.bot // 'shadow:'
        self.mk.bot // '\tgit checkout $@'
        self.mk.bot // '\tgit pull -v'
        # release
        self.mk.bot // 'release:'
        self.mk.bot // '\tgit tag $(NOW)-$(REL)'
        self.mk.bot // '\tgit push -v && git push -v --tags'
        self.mk.bot // '\t$(MAKE) shadow'
        #
        self.mk.sync()

    def init_apt(self):
        self['apt'] = self.apt = File('apt.txt', comment=None)
        self.diroot // self.apt
        #
        self.apt // 'git make wget'
        self.apt.sync()

    def init_giti(self):
        self['gitignore'] = self.giti = File('.gitignore')
        self.diroot // self.giti
        # common files
        self.giti.top // '*~' // '*.swp'
        self.giti.top // '*.log' // '/tmp/'
        #
        self.giti.sync()

## @ingroup prj
class anyModule(dirModule):
    def __init__(self, V=None):
        super().__init__(V)
        self['GITHUB'] = Url('https://repl.it/@metaLmasters/metaL#')
        # LICENSE
        self.lic = File('LICENSE', comment=None)
        self.diroot // self.lic
        self.lic // (
            self['LICENSE'].val +
            self['LICENSE'].nest[0].val.format(
                YEAR=self.YEAR.file(),
                AUTHOR=self.AUTHOR.file(), EMAIL=self.EMAIL.file()
            ))
        self.lic.sync()
        # vscode
        self.init_vscode()
        # tasks
        self.init_tasks()

    def init_vscode(self):
        self.diroot['vscode'] = self.vscode = Dir('.vscode')
        self.diroot // self.vscode
        self.init_settings()
        self.init_launch()

    def init_mk(self):
        super().init_mk()
        # src
        self.mk.src = self['src'] = Section('src')
        self.mk.mid // self.mk.src
        # obj
        self.mk.obj = self['obj'] = Section('obj')
        self.mk.mid // self.mk.obj
        # all
        self.mk.all = self['all'] = Section('all')
        self.mk.mid // self.mk.all
        # rules
        self.mk['rules'] = self.mk.rules = Section('rules')
        self.mk.mid // self.mk.rules
        self.mk.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.bot // ('/%s' % self.val)
        # self.giti.bot // ('/%s.exe\n/%s' % (self.val, self.val))
        # self.giti.bot // '*.o' // '*.objdump'
        self.giti.sync()

    def init_settings(self):
        self.vscode['settings'] = self.settings = File(
            'settings.json', comment='//')
        self.vscode // self.settings
        self.settings.top // '{'
        self.settings.bot // '\t"editor.tabSize": 4,'
        self.settings.bot // '}'
        self.settings.multiCommand = Section('multiCommand', comment='//')
        self.settings.multiCommand // '"multiCommand.commands": ['
        self.settings.f11 = multiCommand('f11', 'make test')
        self.settings.f12 = multiCommand('f12', 'make all')
        self.settings.multiCommand // self.settings.f11 // self.settings.f12
        self.settings.multiCommand // '],'
        self.settings.mid // self.settings.multiCommand
        self.settings.watcher = Section('watcher', comment='//')
        self.settings.mid // '"files.watcherExclude": {'
        self.settings.mid // self.settings.watcher
        self.settings.mid // '},'
        self.settings.exclude = Section('exclude', comment='//')
        self.settings.mid // '"files.exclude": {'
        self.settings.mid // self.settings.exclude
        self.settings.mid // '},'
        self.settings.assoc = Section('associations', comment='//')
        self.settings.mid // '"files.associations": {'
        self.settings.mid // self.settings.assoc
        self.settings.mid // '},'
        self.settings.sync()

    def init_tasks(self):
        self.vscode['tasks'] = self.tasks = File('tasks.json', comment='//')
        self.vscode // self.tasks
        self.tasks.top // '{' // '\t"version": "2.0.0",' // '\t"tasks": ['
        self.tasks.bot // '\t]' // '}'
        self.tasks.sync()

    def init_launch(self):
        self.vscode['launch'] = self.launch = File('launch.json', comment='//')
        self.vscode // self.launch
        self.launch.top // '// https://code.visualstudio.com/docs/python/debugging'
        self.launch.top // '{'
        self.launch.top // '\t"configurations": ['
        self.launch.bot // '\t]'
        self.launch.bot // '}'
        self.launch.sync()

    def mksrc(self, file):
        assert isinstance(file, File)
        self.mk.src // ('SRC += %s' % file.val)

## @defgroup cc ANSI C'99
## @ingroup gen
## @brief ANSI C'99 code generation targeted for @ref tcc

## @ingroup cc
class CC(Object):
    pass

## @ingroup cc
class ccModule(anyModule):
    def init_mk(self):
        super().init_mk()
        #
        self.mk.tools // f'{"TCC":<8} = tcc'
        self.mk.tools // f'{"CC":<8} = $(TCC)'
        self.mk.tools // f'{"CXX":<8} = g++'
        self.mk.tools // f'{"AS":<8} = $(CC)'
        self.mk.tools // f'{"LD":<8} = $(CC)'
        self.mk.tools // f'{"OBJDUMP":<8} = objdump'
        self.mk.tools // f'{"SIZE":<8} = size'
        #
        self.mk['flags'] = self.mk.flags = Section('flags')
        self.mk.top // self.mk.flags
        self.mk.flags // f'{"OPT":<8} = -O0 -g2 '
        self.mk.flags // f'{"CFLAGS":<8} = $(OPT) -I.'
        #
        self.mk.obj // ('OBJ += %s' % self.val)
        #
        self.mk.all // 'all: $(MODULE)'
        self.mk.all // "\t./$^"
        # self.mk.mid // '$(MODULE): $(C) $(H)'
        # self.mk.mid // '\t$(CC) $(CFLAGS) -o $@ $(C)'
        #
        self.mk.sync()
        #
        self.init_h()
        self.init_c()

    def init_h(self):
        self['h'] = self.h = hFile(self.val)
        self.diroot // self.h
        self.h.top // stdlib // stdio
        self.h.top // ccInclude('assert.h')
        self.h.sync()
        self.mk.src // ('H += %s' % self.h.file())

    def init_c(self):
        self['c'] = self.c = cFile(self.val)
        self.diroot // self.c
        # self.c.top // ccInclude(self.h)
        self.c.sync()
        self.mk.src // ('C += %s' % self.c.file())

    def init_apt(self):
        super().init_apt()
        self.apt // 'tcc binutils'
        self.apt.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.mid // '*.exe' // '*.o'
        self.giti.sync()

## @ingroup cc
class cFile(CC, File):
    def __init__(self, V, ext='.c', comment='//'):
        super().__init__(V, ext=ext, comment=comment)
        self.top // ccInclude(self)

## @ingroup cc
class hFile(CC, File):
    def __init__(self, V, ext='.h', comment='//'):
        super().__init__(V, ext=ext, comment=comment)
        self.top // ('#ifndef _%s_H' % V.upper())
        self.top // stdint
        self.bot // ('#endif %s _%s_H' % (comment, V.upper()))


## @ingroup cc
class ccInclude(CC, Module):
    def __init__(self, V):
        if isinstance(V, File):
            V = V.file()
        super().__init__(V)

    def file(self): return '#include <%s>' % self.val


stdint = ccInclude('stdint.h')
stdlib = ccInclude('stdlib.h')
stdio = ccInclude('stdio.h')

## @ingroup cc
## C type
class ccType(CC):
    def file(self): return '%s %s' % (self.cc_type(), self.cc_val())
    ## C type (without first `cc` prefix)
    def cc_type(self): return self._type()[2:]
    ## object value
    def cc_val(self): return '%s' % self.val

class ccInt(ccType):
    pass


ccint = ccInt(0)

## @ingroup cc
class ccVoid(ccType):
    def cc_arg(self): return ''


ccvoid = ccVoid('')


## @ingroup cc
## function
class ccFn(CC, Fn):
    def __init__(self, name, args=ccvoid, returns=ccvoid):
        super().__init__(name)
        assert isinstance(args, Object)
        self['args'] = args
        assert isinstance(returns, Object)
        self['ret'] = returns

    def file(self):
        ret = '\n%s %s(%s) {' % (
            self['ret'].cc_type(), self.val, self['args'].cc_arg())
        for j in self.nest:
            ret += '\n\t%s;' % j.cc_call()
        ret += '\n\treturn %s;\n}' % self['ret'].cc_val()
        return ret

    def cc_call(self):
        return '%s(%s)' % (self.val, self['args'].cc_arg())

    def cc_arg(self):
        return self._val()


## @defgroup py Python
## @ingroup gen

## @ingroup py
class PY(Object):
    pass

## @ingroup py
class pyImport(PY):
    def file(self): return 'import %s' % self.val

## @ingroup py
class pyFn(PY):
    def file(self):
        res = 'def %s():' % self.val
        for i in self.nest:
            res += '\n    ' + i.file()
        return res

## @ingroup py
class pyFile(PY, File):
    def __init__(self, V):
        super().__init__(V, comment='#')
        self.val += '.py'

## @ingroup py
class minpyModule(anyModule):
    def __init__(self, V=None):
        super().__init__(V)
        self.init_py()

    def init_apt(self):
        super().init_apt()
        self.apt // 'python3 python3-venv python3-pip'
        self.apt.sync()

    def init_py(self):
        self.init_reqs()

    def init_reqs(self):
        self.reqs = File('requirements.txt', comment=None)
        self.diroot['reqs'] = self.reqs
        self.diroot // self.reqs
        self.reqs.sync()

    def init_giti(self):
        super().init_giti()
        pygnore = Section('python/venv')
        self.giti.mid // '*.pyc' // '/bin/' // '/include/'
        self.giti.mid // '/lib/' // '/lib64' // '/share/' // '/pyvenv.cfg'
        self.giti.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.tools // '' //\
            f'{"PIP":<8} = $(CWD)/bin/pip3' //\
            f'{"PY":<8} = $(CWD)/bin/python3' //\
            f'{"PYT":<8} = $(CWD)/bin/pytest' //\
            f'{"PEP":<8} = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402' //\
            ''
        self.mk.install //\
            '\t$(MAKE) $(PIP)' //\
            '\t$(PIP) install    -r requirements.txt' //\
            ''
        self.mk.update //\
            '\t$(PIP) install -U    pip' //\
            '\t$(PIP) install -U -r requirements.txt' //\
            ''
        pyinst = Section('py/install')
        self.mk.update.after(pyinst)
        pyinst //\
            '$(PIP) $(PY):' //\
            '\tpython3 -m venv .' //\
            '\t$(PIP) install -U pip pylint autopep8' //\
            '$(PYT):' //\
            '\t$(PIP) install -U pytest' //\
            ''
        # self.mk['all'] = mkall = Section(self)
        # self.mk.mid // mkall
        # mkall['repl'] = repl = Section('repl')
        # mkall // repl
        # repl // '.PHONY: repl\nrepl: $(PY) $(MODULE).py'
        # repl // '\t$(PY) -i $(MODULE).py'
        # repl // '\t$(MAKE) $@'
        self.mk.src // 'SRC += $(MODULE).py'
        self.mk.merge // 'MERGE += $(MODULE).py'
        self.mk.sync()

## @ingroup py
class pyModule(minpyModule):

    def init_giti(self):
        super().init_giti()
        self.giti.bot // (Section('metaL') // ('/%s/' % self.val))
        self.giti.sync()

    def init_settings(self):
        super().init_settings()
        self.settings.top // '    "python.pythonPath": "./bin/python3",'
        self.settings.top // '    "python.formatting.provider": "autopep8",'
        self.settings.top // '    "python.formatting.autopep8Path": "./bin/autopep8",'
        self.settings.top // '    "python.formatting.autopep8Args": ["--ignore=E26,E302,E401,E402"],'
        # self.settings.f11 // 'make repl'
        # self.settings.f12 // 'exit()'
        # files
        t = '\t"**/bin/**": true, "**/include/**":true,'
        self.settings.watcher // t
        self.settings.exclude // t
        t = '\t"**/lib*/**":true, "**/share/**"  :true,'
        self.settings.watcher // t
        self.settings.exclude // t
        t = '\t"**/*.pyc":  true, "**/pyvenv.cfg":true,'
        self.settings.watcher // t
        self.settings.exclude // t
        r = '\t"**/requirements{/**,*}.{txt,in}": "pip-requirements",'
        self.settings.assoc // r
        self.settings.sync()

    def init_launch(self):
        super().init_launch()
        self.launch.mid // '\t\t{'
        self.launch.mid // ('\t\t\t"name": "Python: %s",' % self.val)
        self.launch.mid // '\t\t\t"type": "python",'
        self.launch.mid // '\t\t\t"request": "launch",'
        self.launch.mid // ('\t\t\t"program": "%s.py",' % self.val)
        self.launch.mid // '\t\t\t"console": "integratedTerminal"'
        self.launch.mid // '\t\t}'
        self.launch.sync()

    def init_apt(self):
        super().init_apt()
        self.apt // 'python3 python3-venv python3-pip'
        self.apt.sync()

    def init_py(self):
        try:
            os.symlink('../metaL.py', '%s/metaL.py' % self.diroot.val)
        except FileExistsError:
            pass
        self.py = pyFile(self)
        self.mksrc(self.py)
        # self.py.top // ('## @file %s' % self.file())
        self.diroot['py'] = self.py
        self.diroot // self.py
        self.py['metal'] = self.py.metal = Section('metaL')
        self.py.top // self.py.metal
        self.py['metaimports'] = self.py.metaimports = Section('metaL/imports')
        self.py.metal // self.py.metaimports
        self.py.metaimports // 'from metaL import *'
        self.py.metal // ('MODULE = %s()' % self.__class__.__name__)
        self.py.title = self.py['title'] = Section('title', comment=None)
        self.py.metal // self.py.title
        self.py.title // "TITLE = MODULE['TITLE'] = Title(MODULE)"
        self.py.about = self.py['about'] = Section('about', comment=None)
        self.py.metal // self.py.about
        # self.py.github = self.py['github'] = Section('github', comment=None)
        # self.meta // self.py.github
        self.py.readme = self.py['readme'] = Section('readme', comment=None)
        self.py.metal // self.py.readme
        self.py.readme // 'README = README(MODULE)'
        self.py.readme // 'MODULE.diroot // README'
        self.py.readme // 'README.sync()'
        # meta // ('MODULE = pyModule(\'%s\')' % self.val)
        # meta // ''
        # meta // 'TITLE = Title(\'\')\nMODULE << TITLE'
        # meta // ''
        # meta // '## `~/metaL/$MODULE` target directory for code generation'
        # meta // 'diroot = MODULE[\'dir\']'
        # meta // ''
        # meta // '## README\nreadme = README(MODULE)\ndiroot // readme\nreadme.sync()'
        # meta // ''
        # meta // '## module source code\npy = diroot[\'py\']'
        # meta // "py['head'] // ('## @brief %s' % MODULE['title'].val) // ''"
        # meta // 'py.sync()'
        self.py['tail'] // Section('init')
        self.py.sync()
        # config
        config = pyFile('config')
        self.mksrc(config)
        self.diroot['config'] = config
        self.diroot // config
        config['head'] // '## @brief site-local private config'
        config['head'] // ''
        config['head'] // '## @defgroup config config'
        config['head'] // '## @brief site-local private config'
        config['head'] // '## @{'
        config['tail'] // '\n## @}'
        config.sync()

    def py(self):
        s = '## @brief %s' % self.head(test=True)
        return s

## @ingroup py
class bountyModule(pyModule):
    def __init__(self, V=None):
        pyModule.__init__(self, V)
        self.github = self['GITHUB'] = Url('https://bitbucket.org/ponyatov/')
        self.github['branch'] = '/src/master/'
        self.py.about // "ABOUT = MODULE['ABOUT'] = Url('https://bountify.co/' + MODULE.val)"
        # self.py.github // "GITHUB = MODULE['GITHUB'] = Url('https://bitbucket.org/ponyatov/%s/' % MODULE.val)"
        self.py.sync()


## @defgroup lexer lexer
## @ingroup parser


import ply.lex as lex

## @ingroup lexer
## token types
tokens = ['symbol', 'string',
          'number', 'integer', 'hex', 'bin',
          'lp', 'rp', 'lq', 'rq', 'lc', 'rc',
          'add', 'sub', 'mul', 'div', 'pow',
          'comma', 'tick', 'eq', 'dot', 'colon', 'bar', 'at',
          'nl', 'exit']

## @ingroup lexer
## drop spaces
t_ignore = ' \t\r'

## @ingroup lexer
## line commens starts with `#`
t_ignore_comment = r'\#.*'

## @name string lexer state
## @{

## @ingroup lexer
## lexer states: string parsing mode
states = (('str', 'exclusive'),)

## @ingroup lexer
t_str_ignore = ''

## @ingroup lexer
## start string
def t_str(t):
    r"'"
    t.lexer.string = ''
    t.lexer.push_state('str')
## @ingroup lexer
## end string
def t_str_string(t):
    r"'"
    t.lexer.pop_state()
    t.value = String(t.lexer.string)
    return t
## @ingroup lexer
## mutiline strings processing
def t_str_nl(t):
    r"\n"
    t.lexer.string += t.value
## @ingroup lexer
## `\n`
def t_str_esc_nl(t):
    r"\\n"
    t.lexer.string += '\n'
## @ingroup lexer
## `\r`
def t_str_esc_cr(t):
    r"\\r"
    t.lexer.string += '\r'
## @ingroup lexer
## `\t`
def t_str_esc_tab(t):
    r"\\t"
    t.lexer.string += '\t'
## @ingroup lexer
## any other chars
def t_str_any(t):
    r"."
    t.lexer.string += t.value

## @}


## @ingroup lexer
## increment line counter on every new line
def t_nl(t):
    r'\n'
    t.lexer.lineno += 1
    return t

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

## @ingroup lexer
##    r'`'
def t_tick(t):
    r'`'
    t.value = Op(t.value)
    return t

## @ingroup lexer
##    r'='
def t_eq(t):
    r'='
    t.value = Op(t.value)
    return t

## @ingroup lexer
##    r'\.'
def t_dot(t):
    r'\.'
    t.value = Op(t.value)
    return t

## @ingroup lexer
##    r':'
def t_colon(t):
    r':'
    t.value = Op(t.value)
    return t

## @ingroup lexer
##    r'\|'
def t_bar(t):
    r'\|'
    return t

## @ingroup lexer
def t_at(t):
    r'\@'
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
    r'[^ \t\r\n\#\+\-\*\/\^\\(\)\[\]\{\}\:\=\.\@]+'
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

def p_REPL_nl(p):
    ' REPL : REPL nl '
    p[0] = p[1]

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
## operators precedence
##
## precedence level increases down to the end:
## the lower group has higher precedence
precedence = (
    ('right', 'eq', ),
    ('nonassoc', 'colon', 'dot',),
    ('left', 'add', 'sub'),
    ('left', 'mul', 'div'),
    ('left', 'pow', ),
    ('left', 'pfx', ),
    ('nonassoc', 'tick',),
)

## @ingroup parser
##    ' ex : tick ex '
def p_ex_tick(p):
    ' ex : tick ex '
    p[0] = p[1] // p[2]

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

## @ingroup parser
##    ' ex : ex eq ex '
def p_ex_eq(p):
    ' ex : ex eq ex '
    p[0] = p[2] // p[1] // p[3]

## @ingroup parser
##    ' ex : ex dot ex '
def p_ex_dot(p):
    ' ex : ex dot ex '
    p[0] = p[2] // p[1] // p[3]

## @ingroup parser
##    ' ex : ex colon ex '
def p_ex_colon(p):
    ' ex : ex colon ex '
    p[0] = p[2] // p[1] // p[3]

## @}

## @name (parens)
## @{

## @ingroup parser
##    ' ex : lp ex rp '
def p_ex_parens(p):
    ' ex : lp ex rp '
    p[0] = p[2]

## @}

## @name {functions}
## @{

## @ingroup parser
##    ' ex : ex ex '
def p_ex_apply(p):
    ' ex : ex at ex '
    p[0] = p[2] // p[1] // p[3]

## @ingroup parser
##    ' ex : lc fn rc '
def p_ex_fn(p):
    ' ex : lc fn rc '
    p[0] = p[2]

## @ingroup parser
##    ' fn : '
def p_fn_empty(p):
    ' fn : '
    p[0] = Fn('')

## @ingroup parser
##    ' fn : fn symbol bar '
def p_fn_bar(p):
    ' fn : fn symbol bar '
    p[0] = p[1]
    p[0]['args'] = Vector('')
    p[0]['args'] // p[2]

## @ingroup parser
##    ' fn : fn ex '
def p_fn(p):
    ' fn : fn ex '
    p[0] = p[1] // p[2]

## @}

## @name [vector]
## @{

## @ingroup parser
##    ' ex : lq vector rq '
def p_ex_vector(p):
    ' ex : lq vector rq '
    p[0] = p[2]
## @ingroup parser
##    ' vector : '
def p_vector_empty(p):
    ' vector : '
    p[0] = Vector('')
## @ingroup parser
##    ' vector : vector ex '
def p_vector_single(p):
    ' vector : vector ex '
    p[0] = p[1] // p[2]
## @ingroup parser
##    ' vector : vector comma ex '
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
##    ' ex : string '
def p_ex_string(p):
    ' ex : string '
    p[0] = p[1]
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
    metaL(' {} @ 123 ')
    REPL()
