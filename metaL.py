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
MANIFEST = 'https://github.com/ponyatov/metaL/wiki/metaL-manifest'
## @}

import os, sys, random, re

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
        ## object name / scalar value (string, number,..)
        self.val = V
        ## slots = attributes = dict = env
        self.slot = {}
        ## nested AST = vector = stack = queue
        self.nest = []
        ## parent nodes registry
        self.par = []
        ## global storage id
        ## @ingroup persist
        self.gid = hash(self)#self.sync().gid

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
        tree = self.pad(depth) + self.head(prefix, test)
        # cycles
        if not depth:
            cycle = []
        if self in cycle:
            return tree + ' _/'
        # slot{}s
        for i in sorted(self.slot.keys()):
            tree += self.slot[i].dump(cycle + [self],
                                      depth + 1, f'{i} = ', test)
        # nest[]ed
        for j, k in enumerate(self.nest):
            tree += k.dump(cycle + [self],
                           depth + 1, f'{j}: ', test)
        # subtree
        return tree

    ## paddig for @ref dump
    def pad(self, depth, block=True, tab='\t'):
        if block:
            ret = '\n'
            ret += tab * depth
        else:
            ret = ''
        return ret

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
            return self.slot[key]
            # try:
            #     return self.slot[key]
            # except KeyError:
            #     return Undef(key) // self
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
    def __floordiv__(self, that):
        if isinstance(that, str): # wrap Python string
            that = String(that)
        that.pre__floordiv__(self)
        self.nest.append(that)
        that.post__floordiv__(self)
        return self

    ## pre-callback for `__floordiv__`
    def pre__floordiv__(self, parent): pass

    ## post-callback for `__floordiv__`
    def post__floordiv__(self, parent):
        self.par.append(parent)

    ## @}

    ## @name stack ops
    ## @{

    ## clean `.nest[]`
    def dropall(self):
        self.nest = []
        return self

    ## push to `.nest[]`
    ## @param[in] sync push with sync
    ## @param[in] that `B` operand to be pushed
    def push(self, that):
        return self // that

    ## insert `that` into parent node after the current
    def after(self, that):
        assert len(self.par) == 1
        for parent in self.par:
            index = parent.index(self)
            parent.insert(index + 1, that)
            that.post__floordiv__(parent)
        return self

    ## insert `A[index]=B`
    ## @param[in] index integer indsex in `.nest[]`
    ## @param[in] that `B` operand to be inserted
    def insert(self, index, that):
        self.nest.insert(index, that)
        return self

    def drop(self, count=1):
        for i in range(count):
            self.nest.pop()
        return self

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

    ## comment start (for sigle-line and block comments)
    def comment(self):
        return self.par[0].comment()
    ## comment end (for block comments)

    def commend(self):
        return self.par[0].commend()

    ## default f"format"ting for all nodes
    def __format__(self, spec=None):
        ret = f'{self.val}'
        if 't' in spec:
            ret = ret.title()
        if 'u' in spec:
            ret = ret.upper()
        if 'l' in spec:
            ret = ret.lower()
        return ret

    ## to generic text file: use `.json` in place of `Error`
    ## @ingroup gen

    def file(self, depth=0, tab=None):
        assert tab
        return self.pad(depth, self.par[0].block, tab) + self.json()

    ## @}


## @ingroup object
## nil value
class Nil(Object):
    def __init__(self):
        super().__init__('')

## @defgroup error Error
## @ingroup object

## @ingroup error
class Error(Object, BaseException):
    pass

# ## @ingroup error
# class Undef(Object):
#     pass

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
class Name(Primitive):

    ## names evaluate via context lookup
    def eval(self, ctx): return ctx[self.val]

    ## assignment
    def eq(self, that, ctx):
        ctx[self.val] = that
        return that

## @ingroup prim
class String(Primitive):
    ## @param[in] V string value
    ## @param[in] block source code flag: tabbed blocks or inlined code
    def __init__(self, V, block=True, tab=1):
        super().__init__(V)
        self.block = block
        self.tab = tab
        self.rem = None

    def _val(self):
        s = ''
        v = '' if self.val == None else self.val
        for c in v:
            if c == '\n':
                s += r'\n'
            elif c == '\r':
                s += r'\r'
            elif c == '\t':
                s += r'\t'
            else:
                s += c
        return s

    def file(self, depth=0, tab=None):
        assert tab
        # assert len(self.par) == 1
        ret = self.pad(depth, self.par[0].block, tab) + f'{self.val}'
        if self.val is None:
            ret = ''
        ret += f' {self.rem}' if self.rem else ''
        for i in self.nest:
            ret += i.file(depth + 1, tab)
        return ret

    def py(self): return self.val

    def cc_arg(self): return '"%s"' % self._val()

    def post__floordiv__(self, parent):
        super().post__floordiv__(parent)


## @ingroup prim
## floating point
class Number(Primitive):
    def __init__(self, V):
        Primitive.__init__(self, float(V))

    def file(self, depth=0, tab=None):
        assert tab
        return '%s' % self.val

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
    def __init__(self, V='', nest=None):
        super().__init__(V)
        if nest:
            self.nest = nest

    def eval(self, ctx):
        res = self.__class__(self.val)
        for i in self.nest:
            res // i.eval(ctx)
        return res

    def cc_arg(self):
        ret = ','.join([j.cc_arg() for j in self.nest])
        return '/* %s */ %s' % (self.head(), ret)

## @ingroup cont
class Tuple(Vector):
    def __init__(self, nest=[]):
        super().__init__('')
        for i in nest:
            self // i

    def file(self, depth=0, tab=None):
        return f'{self}'

    def __format__(self, spec):
        assert not spec
        return ', '.join(f'{i.__format__(spec)}' for i in self.nest)

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

    def __init__(self, V, args=[], returns=Nil()):
        super().__init__(V)
        self['args'] = self.args = Args(args)
        self['ret'] = self.ret = returns
        self.block = True

    def eval(self, ctx): return self

    def apply(self, that, ctx):
        self['arg'] = that
        self['ret'] = Nil()
        print('self', self)
        print('that', that)
        return self['ret']

    def at(self, that, ctx): return self.apply(that, ctx)

    def file(self, depth=0, tab=None):
        pfx = ''
        assert tab
        res = self.pad(depth, self.par[0].block, tab)
        res += 'def %s%s(%s):' % (pfx, self.val, self.args.file(tab=tab))
        if not self.nest:
            res += ' pass'
        for i in self.nest:
            res += i.file(depth + 1, tab)
        return res

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
## source code
class S(Meta, String):
    def __init__(self, start=None, end=None, block=True, **kwargs):
        if 'doc' in kwargs:
            String.__init__(self, kwargs['doc'], block, tab=0)
        else:
            String.__init__(self, start, block)
        self.rem = kwargs['rem'] if 'rem' in kwargs else None
        self.end = end

    def file(self, depth=0, tab=None):
        assert tab
        ret = super().file(depth, tab)
        ret += self.file_end(depth, tab)
        return ret

    def file_end(self, depth, tab):
        assert tab
        blocking = self.block if hasattr(self, 'block') else self.par[0].block
        if self.end is None:
            return ''
        elif self.end == '':
            return '\n'
        else:
            return self.pad(depth, blocking, tab) + self.end

class CR(S):
    def __init__(self):
        super().__init__('', block=False)

    def file(self, depth=0, tab=None):
        assert tab
        return '\n'

## @ingroup meta
## commented code block
class D(S):
    def __init__(self, V='', end=None):
        super().__init__(end=end, doc=V)

    def file(self, depth=0, tab=None):
        assert tab
        return super().file(depth - 1, tab)

class H(S):

    def __init__(self, V, *vargs, **kwargs):
        super().__init__(f'{V}', end=None if 0 in vargs else f'</{V}>')
        for i in kwargs:
            self[i] = f'{kwargs[i]}'

    def file(self, depth=0, tab=None):
        assert tab
        assert len(self.par) == 1
        ret = self.pad(depth, self.par[0].block, tab) + f'<{self.val}'
        for i in sorted(self.slot.keys()):
            j = 'class' if i == 'clazz' else i
            j = re.sub(r'_', r'-', j)
            ret += f' {j}="{self.slot[i]}"'
        ret += '>'
        for j in self.nest:
            ret += j.file(depth + 1, tab)
        ret += self.file_end(depth, tab)
        return ret

## @ingroup meta
class Return(S):
    def __init__(self, V):
        super().__init__('return %s' % V)

## @ingroup meta
class Arg(Meta, Name):
    def __int__(self): return self.val

    def file(self, depth=0, tab=' '):
        assert tab
        return f'{self}'

## @ingroup meta
class Args(Meta, Tuple):
    def __init__(self, nest=[]):
        Tuple.__init__(self, nest=nest)
        self.block = False

## @ingroup meta
class Class(Meta):
    def __init__(self, C, sup=None):
        if type(C) == type(Class):
            super().__init__(C.__name__)
            self.C = C
        else:
            super().__init__(C)
        if sup:
            self['sup'] = self.sup = Args(sup)
        self.block = True

    def colon(self, that, ctx):
        return self.C(that)

    def file(self, depth=0, tab=None):
        assert tab
        ret = self.pad(depth, self.par[0].block, tab) + f'class {self}'
        if 'sup' in self.keys():
            ret += f'({self.sup})'
        ret += ':'
        if self.nest:
            for j in self.nest:
                ret += j.file(depth + 1, tab)
        else:
            ret += ' pass'
        return ret

## @ingroup meta
class Method(Meta, Fn):
    pass

## @ingroup meta
class pyInterface(Meta):
    def __init__(self, V, ext=[]):
        super().__init__(V)
        self.block = True
        for i in ext:
            self // i

    def file(self, depth=0, tab=None):
        assert tab
        ret = '\n' + \
            self.pad(depth, self.par[0].block, tab) + f'## @name {self}'
        if 'url' in self.keys():
            ret += self.pad(depth, self.par[0].block,
                            tab=tab) + f"## {self['url']}"
        ret += self.pad(depth, self.par[0].block, tab) + '## @{'
        ret += '\n'
        # z = ''
        for i in self.nest:
            ret += i.file(depth + 0)
        #
        ret += '\n'
        ret += self.pad(depth, self.par[0].block, tab) + '## @}'
        return ret

## @ingroup meta
class Module(Meta):
    def file(self, depth=0, tab=None):
        assert tab
        return self.head(test=True)


vm['module'] = Class(Module)

## @ingroup meta
## text files with any code are devided by sections (can be nested as subsections)
class Section(Meta):
    def __init__(self, V, comment=True):
        super().__init__(V)
        ## every section known its parent: file or other outer section
        assert not self.par
        ## sections always blocked in files
        self.block = True
        if not comment:
            self.comment = lambda: False

    # ## block mutiple parents for all `Section`s
    # def pre__floordiv__(self, parent):
    #     assert not self.par
    #     super().pre__floordiv__(parent)

    def file(self, depth=0, tab=None):
        assert tab
        # assert len(self.par) == 1
        if not self.nest:
            return ''
        #
        comment = self.comment()
        head = self.head(test=True)
        commend = self.commend()
        #
        ret = self.pad(depth, self.par[0].block, tab) if comment else ''
        if comment:
            ret += f'{comment} \\ {head}{commend}'
        for i in self.nest:
            ret += i.file(depth, tab)
        if comment:
            ret += self.pad(depth, self.par[0].block, tab)
            ret += f'{comment} / {head}{commend}'
        return ret


## @defgroup io IO
## @ingroup object
## @brief base file output

## @ingroup io
class IO(Object):
    pass

## @ingroup io
class Dir(IO):

    def sync(self):
        if not self.par:
            try:
                os.mkdir(self.val)
            except FileExistsError:
                pass
        return super().sync()

    def pre__floordiv__(self, parent):
        assert isinstance(parent, Dir)
        super().pre__floordiv__(parent)

    def post__floordiv__(self, parent):
        assert isinstance(parent, Dir)
        super().post__floordiv__(parent)
        try:
            os.mkdir(self.fullpath())
        except FileExistsError:
            pass

    def fullpath(self):
        assert len(self.par) <= 1
        if self.par:
            assert isinstance(self.par[0], Dir)
            return self.par[0].fullpath() + '/' + self.val
        else:
            return self.val

    # ## append file
    # def __floordiv__(self, that):
    #     super().__floordiv__(that)
    #     # if isinstance(that, File):
    #     #     that.fh = open('%s/%s%s' % (self.val, that.val, that.ext), 'w')
    #     #     return IO.__floordiv__(self, that)
    #     # if isinstance(that, Dir):
    #     #     that.val = '%s/%s' % (self.val, that.val)
    #     #     return IO.__floordiv__(self, that)
    #     # raise Error((self))


## @ingroup io
class File(IO):
    ## @param[in] V file name without extension
    ## @param[in] ext file extension (default none)
    ## @param[in] comment syntax comment (depends on a file type)
    def __init__(self, V, ext='', comment='#', tab='\t'):
        ## file handler not assigned on File object creation
        self.fh = None
        ##
        self.comment = lambda: comment
        commends = {'<!--': '-->', '/*': '*/'}
        commend = ' ' + commends[comment] if comment in commends else ''
        self.commend = lambda: commend
        ##
        super().__init__(V)
        self['ext'] = self.ext = ext
        self.tab = tab
        ##
        if comment:
            powered = f"powered by metaL: {MANIFEST}"
            if len(comment) == len('#'):
                self // f"{comment}  {powered}{commend}"
                # self // f"{comment*2} @file{commend}"
            elif len(comment) >= len('//'):
                self // f"{comment} {powered}{commend}"
                # self // f"{comment*2} @file{commend}"
            else:
                raise Error((self.comment))
        ## every file has `top` section
        self.top = Section('top')
        self['top'] = self.top
        self // self.top
        ## every file has `mid`ddle section
        self.mid = Section('mid')
        self['mid'] = self.mid
        self // self.mid
        ## every file has `bot`tom section
        self.bot = Section('bot')
        self['bot'] = self.bot
        self // self.bot
        ## all files holds tab-blocked sections/strings
        self.block = True

    def pre__floordiv__(self, parent):
        assert isinstance(parent, Dir)
        super().pre__floordiv__(parent)

    def post__floordiv__(self, parent):
        assert isinstance(parent, Dir)
        super().post__floordiv__(parent)
        self.fh = open(self.fullpath(), 'w')

    def fullpath(self):
        assert len(self.par) == 1
        assert isinstance(self.par[0], Dir)
        return self.par[0].fullpath() + '/' + self.val + self.ext

    def __format__(self, spec):
        assert not spec
        return f'{self.val}{self.ext}'

    def file(self, depth=0, tab=None):
        assert tab
        ret = ''
        for j in self.nest:
            ret += j.file(depth, tab)
        if ret:
            assert ret[0] == '\n'
            ret = ret[1:] + '\n'
        return ret

    def sync(self):
        if self.fh:
            self.fh.seek(0)
            self.fh.write(self.file(tab=self.tab))
            self.fh.truncate()
            self.fh.flush()
        return super().sync()

    # ## push object/line
    # ## @param[in] that `B` operand: string of section will be pushed into file
    # ## @param[in] sync `=False` default w/o flush to disk (via `sync()``)
    # def __floordiv__(self, that, sync=False):
    #     return super().__floordiv__(that, sync)

## @defgroup net net
## @brief Networking
## @ingroup io

## @ingroup net
## networking object
class Net(IO):
    pass

## @ingroup net
## TCP/IP address
class Ip(Net):
    def __format__(self, spec):
        assert not spec
        return f'{self.val}'

## @ingroup net
## TCP/IP port
class Port(Net):
    pass

## @ingroup net
class Email(Net):
    def file(self, depth=0, tab=None):
        assert tab
        return '<%s>' % self.val

    def __format__(self, spec):
        assert not spec
        return f'<{self.val}>'

## @ingroup net
class Url(Net):
    def file(self, depth=0, tab=None):
        assert tab
        return self.pad(depth, self.par[0].block, tab) + self.val

    def __format__(self, spec):
        assert not spec
        return f'{self.val}'

## @ingroup net
class GitHub(Url):
    def __init__(self, V, module=None, branch='master'):
        super().__init__(V)
        self['module'] = self.module = module
        self['branch'] = self.branch = branch

    def __format__(self, spec):
        assert not spec
        return f'{self.val}/metaL/tree/{self.branch}/{self.module}'

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
    def file(self, depth=0, tab=None):
        assert tab
        return f'{self}'

## @ingroup doc
class Color(Doc):
    pass

## @ingroup doc
class Title(Doc):
    ## @ingroup py
    def py(self): return '## @brief %s' % self.val

## @ingroup doc
class Author(Doc):
    pass


from license import License, MIT

## @defgroup gui GUI
## @brief Generic GUI

## @ingroup gui
class GUI(Object):
    pass

## @ingroup gui
class Window(GUI):
    def htdump(self):
        ret = self.dump()
        ret = re.sub(r'\<', r'&lt', ret)
        ret = re.sub(r'\>', r'&gt', ret)
        return ret

    def html(
        self): return f'<div class="window"><pre>{self.htdump()}</pre></div>'


## @ingroup info
## @{
vm['MODULE'] = vm.MODULE = Module(MODULE)
vm['TITLE'] = vm.TITLE = Title(TITLE)
vm['ABOUT'] = vm.ABOUT = String(ABOUT)
vm['EMAIL'] = vm.EMAIL = Email(EMAIL)
vm['AUTHOR'] = vm.AUTHOR = Author(AUTHOR) << EMAIL
vm['YEAR'] = vm.YEAR = Integer(YEAR)
vm['LICENSE'] = vm.LICENSE = MIT
vm['GITHUB'] = vm.GITHUB = GitHub(GITHUB, MODULE)
vm['LOGO'] = vm.LOGO = File(LOGO, comment=None)
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
        self // (f'## {module["TITLE"]}')
        # self // ''
        about = module['ABOUT'].val
        while about and about[-1] in '\r\n':
            about = about[:-1]
        about += '\n* powered by `metaL`'
        self // ('%s' % about)
        self // ''
        self // ('(c) %s <<%s>> %s %s' % (
            module['AUTHOR'].val, module['EMAIL'].val,
            module['YEAR'].val, module['LICENSE'].val))
        self.github = Section('github')
        self // self.github
        self.github // '' // f"github: {module['GITHUB']}" // ''
        # install
        self.install = Section('install')
        self // self.install
        self.install // '## Install' //\
            self.module.readme.install
        # tutorial
        self.tutorial = Section('tutorial')
        self // self.tutorial
        self.tutorial // '## Tutorial' //\
            self.module.readme.tutorial
        # self.module.init_readme_tutorial()


## @ingroup prj
class Makefile(File):
    def __init__(self, V='Makefile'):
        super().__init__(V, comment='#', tab='\t')

## @ingroup prj
## system setting
class Setting(Meta):
    def __init__(self, key, val):
        super().__init__(key)
        self.key = key
        self // val
        self.block = True

    def __floordiv__(self, that):
        self.nest = []
        Meta.__floordiv__(self, that)

## @ingroup prj
## VSCode multicommand
class multiCommand(S):
    def __init__(self, key, cmd):
        super().__init__('{"command": "multiCommand.%s", ' % key, '},')
        self.cmd = String(cmd)
        self // (S('"sequence":[', ']') //
                 '"workbench.action.files.saveAll",' //
                 (S('{"command": "workbench.action.terminal.sendSequence",', '}') //
                  (S('"args": {', '}', block=False) //
                   (S('"text": "\\u000D', '\\u000D"', block=False) //
                    self.cmd
                    ))))

## @defgroup dirmod dirModule
## @ingroup prj
## module with its own directory (root module = project)

## @ingroup dirmod
## module with its own directory (root module = project)
##
## https://www.notion.so/metalang/The-base-of-all-projects-dirModule-f6f20d6dd12b42738dd2a8aee7cc8a42
class dirModule(Module):
    ## @param[in] V default name is the current file name
    def __init__(self, V=None):
        # current file name
        if not V:
            V = __import__('sys').argv[0]
            V = V.split('/')[-1]
            V = V.split('.')[0]
        super().__init__(V)
        # fill metainformation from VM (metaL author/info)
        self['TITLE'] = self.TITLE = Title(self)
        self['ABOUT'] = self.ABOUT = String('\n')
        self['AUTHOR'] = self.AUTHOR = vm['AUTHOR']
        self['EMAIL'] = self.EMAIL = vm['EMAIL']
        self['YEAR'] = self.YEAR = vm['YEAR']
        self['LICENSE'] = self.LICENSE = vm['LICENSE']
        self['GITHUB'] = self.GITHUB = GitHub(GITHUB, self)
        # diroot: directory with same name as the module
        self['dir'] = self.diroot = Dir(V).sync()
        #
        self.init_first()
        # apt.txt
        self.init_apt()
        # gitignore
        self.init_giti()
        # tmp
        self.init_dirs()
        # Makefile
        self.init_mk()
        # README
        self.init_readme()

    def init_first(self): pass

    def init_dirs(self):
        self['tmp'] = self.tmp = Dir('tmp')
        self.diroot // self.tmp
        self.tmp.giti = File('.gitignore')
        self.tmp // self.tmp.giti
        self.tmp.giti // '*.zip'
        self.tmp.giti.sync()

    ## create defaut Makefile
    def init_mk(self):
        self.diroot['mk'] = self.mk = Makefile()
        self['mk'] = self.mk
        self.diroot // self.mk
        # vars
        self.mk['vars'] = self.mk.vars = Section('vars')
        self.mk.top // self.mk.vars
        # module
        self.mk['module'] = self.mk.module = Section('module')
        self.mk.module // f'{"MODULE":<8} = $(notdir $(CURDIR))'
        self.mk.vars // self.mk.module
        self.mk.vars // f'{"OS":<7} ?= $(shell uname -s)'
        # version
        self.mk['version'] = self.mk.version = Section('version')
        self.mk.top // self.mk.version
        self.mk.version // f'{"NOW":<8} = $(shell date +%d%m%y)'
        self.mk.version // f'{"REL":<8} = $(shell git rev-parse --short=4 HEAD)'
        # dirs
        self.mk['dirs'] = self.mk.dirs = Section('dirs')
        self.mk.top // self.mk.dirs
        self.mk.dirs //\
            f'{"CWD":<8} = $(CURDIR)' //\
            f'{"BIN":<8} = $(CWD)/bin' //\
            f'{"LIB":<8} = $(CWD)/lib' //\
            f'{"TMP":<8} = $(CWD)/tmp' //\
            f'{"SRC":<8} = $(CWD)/src' //\
            f'{"GZ":<8} = $(HOME)/gz'
        # tools
        self.mk['tools'] = self.mk.tools = Section('tools')
        self.mk.top // self.mk.tools
        self.mk.xpath = Section('xpath', 0) //\
            f'{"XPATH":<8} = PATH=$(BIN):$(PATH)'
        self.mk.tools //\
            f'{"WGET":<8} = wget -c --no-check-certificate' //\
            f'{"CORES":<8} = $(shell grep proc /proc/cpuinfo|wc -l)' //\
            self.mk.xpath //\
            f'{"XMAKE":<8} = $(XPATH) $(MAKE) -j$(CORES)'
        # lib
        self.mk.lib = self['lib'] = Section('lib')
        self.mk.mid // self.mk.lib
        # src
        self.mk.src = self['src'] = Section('src')
        self.mk.mid // self.mk.src
        # obj
        self.mk.obj = self['obj'] = Section('obj')
        self.mk.mid // self.mk.obj
        # all
        self.mk.all = self['all'] = Section('all')
        self.mk.all.targets = S('all:', block=False)
        self.mk.mid // ((D('.PHONY: all') //
                         self.mk.all.targets //
                         (S() //
                          self.mk.all //
                          '$(MAKE) test'
                          )))
        # test
        self.mk.test = self['test'] = Section('test', comment=None) // '$^'
        self.mk.test.targets = S('test:', block=False)
        self.mk.mid // ((D('.PHONY: test') //
                         self.mk.test.targets //
                         (S() //
                          self.mk.test)))
        # repl
        self.mk.repl = self['repl'] = Section('repl')
        self.mk.repl.targets = S('repl:', block=False)
        self.mk.mid // ((D('.PHONY: repl') //
                         self.mk.repl.targets //
                         (S() //
                          '$(MAKE) test' //
                          self.mk.repl //
                          '$(MAKE) $@')))
        # rules
        self.mk.rules = self['rules'] = Section('rules')
        self.mk.mid // self.mk.rules
        # doc
        self.mk.doc = Section('doc')
        self.mk.doc.doc = S('.PHONY: doc\ndoc:', '', 0)
        self.mk.mid // (self.mk.doc // self.mk.doc.doc)
        # install
        install = Section('install')
        self.mk.bot // install
        self.mk.install = S('install:') // '$(MAKE) $(OS)_install'
        install // '.PHONY: install' // self.mk.install
        self.mk.install // '$(MAKE) doc'
        # update
        update = Section('update')
        self.mk.bot // update
        self.mk.update = S('update:') // '$(MAKE) $(OS)_update'
        update // '.PHONY: update' // self.mk.update
        self.mk['linux'] = self.mk.linux = Section('linux/install')
        self.mk.bot // self.mk.linux
        self.mk.linux // '.PHONY: Linux_install Linux_update'
        self.mk.linux // (S('Linux_install Linux_update:') //
                          '-sudo apt update' //
                          '-sudo apt install -u `cat apt.txt`')
        # merge master/shadow
        self.mk['merge'] = self.mk.merge = Section('merge')
        self.mk.bot // self.mk.merge
        self.mk.merge // f'MERGE  = {self.mk} {self.apt} {self.giti} .vscode'
        self.mk.merge // 'MERGE += doc src tmp README.md'
        self.mk.bot // S('.PHONY: master shadow release zip', '')
        # master
        self.mk.bot // (S('master:', '') //
                        'git checkout $@' //
                        'git pull -v' //
                        'git checkout shadow -- $(MERGE)')
        # shadow
        self.mk.bot // (S('shadow:', '') //
                        'git checkout $@' //
                        'git pull -v')
        # release
        self.mk.bot // (S('release:', '') //
                        'git tag $(NOW)-$(REL)' //
                        'git push -v && git push -v --tags' //
                        '$(MAKE) shadow')
        # zip
        self.mk.bot // (S('zip:') //
                        'git archive --format zip \\' //
                        '--output ~/tmp/$(MODULE)_src_$(NOW)_$(REL).zip \\' //
                        'HEAD')
        #
        self.mk.sync()

    ## create `apt.txt` with packages must be installed on Debian GNU/Linux
    def init_apt(self):
        self['apt'] = self.apt = File('apt.txt', comment='')
        self.diroot // self.apt
        self.apt // 'git make wget'
        self.apt.sync()

    ## `.gitignore` file masks will not included into repository
    def init_giti(self):
        self['gitignore'] = self.giti = File('.gitignore')
        self.diroot // self.giti
        self.giti.top // '*~' // '*.swp' // '*.log'
        return self.giti.sync()

    def init_readme(self):
        self.readme = Section('readme')
        self.readme.preinstall = Section(
            'preinstall') // self.readme_preinstall()
        self.readme.postinstall = Section(
            'postinstall') // self.readme_postinstall()
        self.readme.install = Section('install') //\
            self.readme.preinstall //\
            (S("\n```", "```\n") //
             f"~$ git clone --depth 1 -o gh https://github.com/ponyatov/metaL ~/metaL" //
             f"~$ cd ~/metaL/{self}" //
             f"~/metaL/{self}$ make install") //\
            self.readme.postinstall
        self.readme.tutorial = Section('tutorial') // self.readme_tutorial()

    def readme_preinstall(self): return ''
    def readme_postinstall(self): return ''
    def readme_tutorial(self): return ''

## @ingroup prj
## extended project template includes some IDE configs and build script extensions
##
## https://www.notion.so/metalang/extending-very-minimal-dirModule-to-more-general-anyModule-5286e00adefe4366925aeba6f7293a1d
class anyModule(dirModule):
    def __init__(self, V=None):
        super().__init__(V)
        self.init_lic()
        self.init_vscode()
        self.init_doc()
        self.init_config()

    def init_config(self):
        self.config = Dict('config')
        #
        import uuid
        secret_key = xxhash.xxh64(str((uuid.getnode(), self))).hexdigest()
        self.config['secret_key'] = self.config.secret_key = secret_key
        #
        self.config['host'] = self.config.host = Ip('127.0.0.1')
        #
        import crc16

        def port_scale(port):
            return int(1024 + ((0xBFFF - 1024) / (0xFFFF)) * port)
        self.config['port'] = self.config.port = port_scale(
            crc16.crc16xmodem(self.val.encode('utf8')))
        assert self.config.port in range(1024, 0xBFFF)

    def init_doc(self):
        self['doc'] = self.doc = Dir('doc')
        self.diroot // self.doc
        self.doc.giti = File('.gitignore')
        self.doc // self.doc.giti
        self.doc.giti // '*.pdf'
        self.doc.giti.sync()

    def init_lic(self):
        self.lic = File('LICENSE', comment=None)
        self.diroot // self.lic
        L = vm['LICENSE']
        self.lic //\
            f'{L}' //\
            L[0].val.format(
                YEAR=f'{self.YEAR}',
                AUTHOR=f'{self.AUTHOR}',
                EMAIL=f'{self.EMAIL}'
            )
        self.lic.sync()

    def init_vscode(self):
        self.diroot['vscode'] = self.vscode = Dir('.vscode')
        self.diroot // self.vscode
        self.init_vscode_settings()
        self.init_vscode_launch()
        self.init_vscode_tasks()
        self.init_vscode_ext()

    def init_mk(self):
        super().init_mk()
        # rules
        self.mk['rules'] = self.mk.rules = Section('rules')
        self.mk.mid // self.mk.rules
        self.mk.sync()

    def init_bin(self):
        self.bin = Dir('bin')
        self.diroot // self.bin
        self.bin.giti = File('.gitignore')
        self.bin // self.bin.giti
        self.bin.giti.sync()

    def init_dirs(self):
        super().init_dirs()
        self.init_bin()
        #
        self['src'] = self.src = Dir('src')
        self.diroot // self.src
        self.src.giti = File('.gitignore')
        self.src // self.src.giti
        self.src.giti.sync()

    # def init_giti(self):
    #     # self.giti.bot // ('/%s' % self.val)
    #     # self.giti.bot // ('/%s.exe\n/%s' % (self.val, self.val))
    #     # self.giti.bot // '*.o' // '*.objdump'
    #     # return self.giti.sync()

    def init_vscode_settings(self):
        settings = File('settings.json', comment='//')
        self.vscode['settings'] = self.vscode.settings = settings
        self.vscode // self.vscode.settings
        settings.top // '{'
        settings.bot // '\t"editor.tabSize": 4,'
        settings.bot // '}'
        #
        self.f9 = multiCommand('f9', 'make all')
        self.f11 = multiCommand('f11', 'make repl')
        self.f12 = multiCommand('f12', 'exit()')
        settings.mid //\
            (Section('multiCommand') //
             (S('"multiCommand.commands": [', '],') //
              self.f9 // self.f11 // self.f12
              )
             )
        #
        watcher = Section('watcher')
        self.vscode['watcher'] = self.vscode.watcher = watcher
        settings.mid // (S('"files.watcherExclude": {', '},') // watcher)
        #
        exclude = Section('exclude')
        self.vscode['exclude'] = self.vscode.exclude = exclude
        settings.mid // (S('"files.exclude": {', '},') // exclude)
        #
        assoc = Section('assoc')
        self.vscode['assoc'] = self.vscode.assoc = assoc
        settings.mid // (S('"files.associations": {', '},') // assoc)
        assoc //\
            '"*{rc,sh}": "shellscript",' //\
            '"ws.?":"json",'
        #
        settings.sync()

    def vs_task(self, target, group='make'):
        return (S('{', '},') //
                f'"label": "{group}: {target}",' //
                '"type": "shell",' //
                f'"command": "make {target}",' //
                '"problemMatcher": [],'
                )

    def vs_make(self, target, group='make'):
        return self.vs_task(target, group)

    def vs_git(self, target, group='git'):
        return self.vs_task(target, group)

    def init_vscode_tasks(self):
        self.vscode['tasks'] = self.tasks = File('tasks.json', comment='//')
        self.vscode // self.tasks
        self.tasks.it = S('"tasks": [', ']')
        self.tasks // (S('{', '}') // '"version": "2.0.0",' // self.tasks.it)
        self.tasks.it //\
            self.vs_make('install') //\
            self.vs_make('update') //\
            self.vs_git('master') //\
            self.vs_git('shadow')
        self.tasks.sync()

    def init_vscode_ext(self):
        self.vscode['ext'] = self.vscode.ext = File(
            'extensions.json', comment='//')
        self.vscode // self.vscode.ext
        self.vscode.ext.top // '{'
        self.vscode.ext.ext = Section('ext') // '"stkb.rewrap",'
        self.vscode.ext.mid //\
            (S('"recommendations": [', ']') // self.vscode.ext.ext)
        self.vscode.ext.bot // '}'
        self.vscode.ext.sync()

    def init_vscode_launch(self):
        launch = File('launch.json', comment='//')
        self.vscode['launch'] = self.vscode.launch = launch
        self.vscode // launch
        launch.top // '// https://code.visualstudio.com/docs/python/debugging'
        launch.top // '{'
        launch.bot // '}'
        #
        launch['it'] = launch.it = Section('')
        launch.mid // (S('"configurations": [', ']') // launch.it)
        launch.sync()

    def mksrc(self, file):
        assert isinstance(file, File)
        self.mk.src // f'SRC += {file}'

    def file(self, depth=0, tab=None):
        assert tab
        return f'{self.__class__.__name__}:{self._val()}'

## @defgroup cc ANSI C'99
## @ingroup gen
## @brief ANSI C'99 code generation targeted for @ref tcc

## @ingroup cc
class CC(Object):
    pass

## @ingroup cc
## generic ANSI C module (POSIX)
class cModule(anyModule):

    def __init__(self, V=None):
        super().__init__(V)
        self.init_c()
        self.init_h()

    def init_c(self):
        self.c = cFile(self)
        self.src // self.c
        self.c.top // cInclude(f'{self}')
        self.c.sync()

    def init_h(self):
        self.h = hFile(self)
        self.h.top // stdlib // stdio // stdass
        self.src // self.h
        self.h.sync()

    def mixin_apt(self):
        self.apt // 'build-essential tcc'
        self.apt.sync()

    def init_apt(self):
        super().init_apt()
        self.mixin_apt()

    def init_giti(self):
        super().init_giti()
        self.giti.mid // '*.exe' // '*.o' // f'/bin/{self:m}'
        return self.giti.sync()

    def __mixin__(self):
        cModule.mixin_mk(self)
        cModule.mixin_apt(self)

    def mixin_mk(self):
        #
        self.mk.tools // f'{"TCC":<8} = tcc'
        self.mk.tools // f'{"CC":<8} = $(TCC)'
        self.mk.tools // f'{"CXX":<8} = g++'
        self.mk.tools // f'{"AS":<8} = $(CC)'
        self.mk.tools // f'{"LD":<8} = $(CC)'
        self.mk.tools // f'{"OBJDUMP":<8} = objdump'
        self.mk.tools // f'{"SIZE":<8} = size'
        #
        self.mk.sync()

    def init_mk(self):
        super().init_mk()
        self.mixin_mk()
        #
        self.mk['flags'] = self.mk.flags = Section('flags')
        self.mk.top // self.mk.flags
        self.mk.flags // f'{"OPT":<8} = -O0 -g2'
        self.mk.flags // f'{"CFLAGS":<8} = $(OPT) -I$(SRC) -I$(TMP)'
        #
        self.mk.obj // f'{"OBJ":<7} += $(TMP)/{self}.o'
        #
        # self.mk.all.targets // ' $(BIN)/$(MODULE)'
        self.mk.test.targets // ' $(BIN)/$(MODULE)'
        #
        self.mk.rules //\
            (S('$(BIN)/$(MODULE): $(OBJ)') //
             '$(CC) $(CFLAGS) -o $@ $^'
             )
        for i in ['SRC', 'TMP']:
            cc = '$(CC) $(CFLAGS) -o $@ -c $<'
            mh = '$(SRC)/$(MODULE).h'
            self.mk.rules //\
                (S(f'$(TMP)/%.o: $({i})/%.c {mh} $({i})/%.h') // cc) //\
                (S(f'$(TMP)/%.o: $({i})/%.c {mh}') // cc)
        #
        self.mk.sync()

    def mixin_ragel(self):
        (self.apt // 'ragel').sync()
        (self.giti // '/tmp/ragel.c').sync()
        #
        self.mk.tools // f'{"RAGEL":<8} = ragel'
        self.mk.obj // f'{"OBJ":<7} += $(TMP)/ragel.o'
        self.mk.rules //\
            (S('$(SRC)/ragel.c: $(SRC)/$(MODULE).ragel') //
                '$(RAGEL) -G2 -o $@ $<')
        self.mk.mid //\
            '.PHONY: ragel\nragel: $(SRC)/ragel.c'
        self.mk.sync()
        #
        self.h.mid //\
            'extern void parse(unsigned char *p , unsigned char *pe);' //\
            'extern void token(char *name, unsigned char *ts, unsigned char *te);'
        self.h.sync()
        #
        self.ragel = cFile(f'{self:m}', ext='.ragel', comment='//')
        self.src // self.ragel
        self.ragel.top //\
            f'#include <{self:m}.h>'
        self.ragel.rex = Section('rex', comment=None) //\
            r"eol = '\r'?'\n';" //\
            r'ws  = [ \t];'
        self.ragel.scan = Section('scanner', comment=None)
        self.ragel.mid //\
            (S('%%{', '}%%') //
             f'machine {self:m};' //
             'alphtype unsigned char;' //
             self.ragel.rex //
             (S(f'{self:m} := |*', '*|;') //
              self.ragel.scan //
              'eol => {token("eol",ts,ts);};'
              )
             )
        self.ragel.sync()

    def mixin_skelex(self):
        self.mk.skelex = Section('skelex')
        self.mk.rules // self.mk.skelex
        self.mk.tools //\
            f'{"LEX":<8} = flex' //\
            f'{"YACC":<8} = bison'
        self.mk.obj //\
            'OBJ += $(TMP)/lexer.o' //\
            'OBJ += $(TMP)/parser.o'
        self.mk.skelex //\
            (S('$(TMP)/lexer.c: $(SRC)/lexer.lex') //
                '$(LEX) -o $@ $<') //\
            (S('$(TMP)/parser.c: $(SRC)/parser.yacc') //
                '$(YACC) -o $@ $<') //\
            '$(TMP)/parser.h: $(TMP)/parser.c' //\
            '$(SRC)/$(MODULE).h: $(TMP)/parser.h'
        self.mk.sync()
        #
        lexinc = (S('%{', '%}') // (S() // cInclude(f'{self}')))
        self.lex = lexFile('lexer')
        self.src // self.lex
        self.lex.comments = Section('comments')
        self.lex //\
            lexinc //\
            '%option yylineno noyywrap' //\
            '%%' //\
            self.lex.comments //\
            f'{".":<8} {{yyerror("lexer");}}' //\
            '%%'
        self.lex.sync()
        #
        self.yacc = yaccFile('parser')
        self.src // self.yacc
        self.yacc.union = Section('union')
        YYERR = '"\\n\\n%i: %s [%s]\\n\\n",yylineno,msg,yytext'
        self.yacc //\
            lexinc //\
            '%defines' //\
            (S('%union {', '}') // self.yacc.union) //\
            '%%' //\
            'REPL:' //\
            '%%' //\
            (S('void yyerror(char *msg) {', '}') //
             f'fprintf(stderr,{YYERR});' //
             'fflush(stderr);' //
             'exit(-1);'
             )
        self.yacc.sync()
        #
        self.h // (Section('parser') //
                   'extern int yylex();' //
                   'extern char* yytext;' //
                   'extern FILE* yyin;' //
                   'extern int yyparse();' //
                   'extern void yyerror(char*);' //
                   'extern int yylineno;' //
                   cInclude(f'parser'))
        self.h.sync()
        #
        (self.tmp.giti // 'lexer.*' // 'parser.*').sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext //\
            '"ms-vscode.cpptools",'
        #  // '"tintinweb.vscode-decompiler",'
        self.vscode.ext.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        #
        self.vscode.cpp = jsonFile('c_cpp_properties')
        self.vscode // self.vscode.cpp
        include = \
            '"includePath": ["${workspaceFolder}/src/**", "${workspaceFolder}/tmp/**"],'
        linux = \
            (S('{', '}') //
             '"name": "Linux",' //
             '"compilerPath": "/usr/bin/tcc",' //
             include //
             '"cStandard": "c99"'
             )
        self.vscode.cpp //\
            '// https://code.visualstudio.com/docs/cpp/c-cpp-properties-schema-reference' //\
            (S('{', '}') //
             (S('"configurations": [', '],') //
                 linux
              ) //
             '"version": 4'
             )
        self.vscode.cpp.sync()
        #
        self.vscode.watcher //\
            '"**/*.o":true,' //\
            f'"bin/{self:m}":true,'
        self.vscode.assoc //\
            '"*.[c|h]":"c",'
        self.vscode.settings.sync()

## @ingroup cc
## cross-compiler module / embedded C/C++
class ccModule(cModule):

    def __mixin__(self):
        cModule.mixin(self)

    def init_mk(self):
        super().init_mk()
        #
        self.mk.all // 'all: $(MODULE)'
        self.mk.all // "\t./$^"
        # self.mk.mid // '$(MODULE): $(C) $(H)'
        # self.mk.mid // '\t$(CC) $(CFLAGS) -o $@ $(C)'
        #
        self.mk.sync()

    def init_h(self):
        self['h'] = self.h = hFile(self.val)
        self.diroot // self.h
        self.h.top // "ccInclude('assert.h')"
        self.h.sync()
        self.mk.src // ('H += %s' % self.h.file())

    def init_c(self):
        self['c'] = self.c = cFile(self.val)
        self.diroot // self.c
        # self.c.top // ccInclude(self.h)
        self.c.sync()
        self.mk.src // ('C += %s' % self.c.file())


## @ingroup cc
class cFile(File):
    def __init__(self, V, ext='.c', comment='//'):
        super().__init__(V, ext=ext, comment=comment, tab=' ' * 4)

## @ingroup cc
class lexFile(File):
    def __init__(self, V, ext='.lex'):
        super().__init__(V, ext=ext, comment=None, tab=' ' * 4)
## @ingroup cc
class yaccFile(File):
    def __init__(self, V, ext='.yacc', comment='/*'):
        super().__init__(V, ext=ext, comment=comment, tab=' ' * 4)

## @ingroup cc
class cInclude(CC, Module):
    def __init__(self, V):
        if isinstance(V, File):
            V = V.file()
        super().__init__(V)

    def file(self, depth=0, tab=None):
        assert tab
        return f'\n#include <{self}.h>'


## @ingroup cc
stdint = cInclude('stdint')
## @ingroup cc
stdlib = cInclude('stdlib')
## @ingroup cc
stdio = cInclude('stdio')
## @ingroup cc
stdass = cInclude('assert')

## @ingroup cc
class hFile(CC, File):
    def __init__(self, V, ext='.h', comment='//'):
        super().__init__(V, ext=ext, comment=comment)
        self.top //\
            f'#ifndef _{V:u}_H'
        self.bot //\
            f'#endif {comment} _{V:u}_H'

## @ingroup cc
## C type
class cType(CC):
    def file(self, depth=0, tab=None):
        assert tab
        return '%s %s' % (self.cc_type(), self.cc_val())

    def __format__(self, spec):
        if spec in ['']:
            return f'{self:t} {self:v}'
        if spec in ['v']:
            return f'{self.val}'
        if spec in ['t']:
            return f'{self._type()[1:]}'
        raise TypeError(spec)

    def file(self, depth=0, tab=None):
        return f'{self:t} {self:v}'

class cInt(cType):
    def __init__(self, V=0):
        super().__init__(V)


cint = cInt()

## @ingroup cc
class cVoid(cType):
    def __init__(self, V=''):
        super().__init__(V)

    def cc_arg(self): return ''


cvoid = cVoid()

## @ingroup cc
class cArgs(Tuple):
    pass

## @ingroup cc
## function
class cFn(CC, Fn):

    def file(self, depth=0, tab=None):
        assert tab
        ret = self.pad(depth, self.par[0].block, tab) + \
            f'{self["ret"]:t} {self}({self["args"]}) {{'
        for j in self.nest:
            ret += j.file(depth + 1, tab)
        ret += self.pad(depth + 1,
                        self.par[0].block, tab) + f'return {self["ret"]:v};'
        ret += self.pad(depth, self.par[0].block, tab) + f'}}'
        return ret

    # # def cc_call(self):
    # #     return '%s(%s)' % (self.val, self['args'].cc_arg())

    # # def cc_arg(self):
    # #     return self._val()


## @ingroup cc
argc = cInt('argc')
## @ingroup cc
argv = Arg('char *argv[]')
## @ingroup cc
main = cFn('main', [argc, argv], returns=cint)


## @defgroup py Python
## @ingroup gen

## @ingroup py
class PY(Object):
    pass

## @ingroup py
class pyImport(PY):
    def file(self, depth=0, tab=None):
        assert tab
        assert len(self.par) == 1
        return self.pad(depth, self.par[0].block, tab) + 'import %s' % self.val

## @ingroup py
class pyFn(PY, Fn):
    ## self-copy
    def cp(self):
        assert not self.nest
        ret = self.__class__(self.val)
        ret.args.dropall()
        for i in self.args:
            ret.args // i
        return ret

## @ingroup py
class pyFile(PY, File):
    def __init__(self, V, ext='.py', comment='#', tab=' ' * 4):
        super().__init__(V, ext, comment, tab)

    # def __format__(self, spec): return f'{self.val}.{self.ext}

## @ingroup py
class pyClass(Class):
    pass

## @ingroup py
class pyMethod(pyFn):
    def __init__(self, V, args=[]):
        super().__init__(V)
        self.block = True
        self['args'] = self.args = Args(nest=[arg for arg in ['self'] + args])

## @ingroup py
class pytestFile(pyFile):
    def __init__(self, py):
        super().__init__('test_%s' % py.val)
        self.top // pyImport('pytest')
        self['none'] = self.none = pyTest('none')
        self.top // self.none
        # self.sync()

## @ingroup py
class pyTest(pyFn):
    def __init__(self, V):
        super().__init__(f'test_{V}')

## @ingroup py
class pyModule(anyModule):
    def __init__(self, V=None):
        self.reqs = File('requirements.pip', comment=None)
        super().__init__(V)
        self.init_reqs()
        self.init_py()

    def init_apt(self):
        super().init_apt()
        self.apt // 'python3 python3-venv python3-pip'
        self.apt.sync()

    def init_reqs(self):
        self.diroot['reqs'] = self.reqs
        self.diroot // self.reqs
        self.reqs // 'xxhash' // 'ply'
        self.reqs.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.mid // '*.pyc' // '/bin/' // '/include/'
        self.giti.mid // '/lib/' // '/lib64' // '/share/' // '/pyvenv.cfg'
        self.giti.mid // '/__pycache__/' // '/.pytest_cache/' // 'config.py'
        return self.giti.sync()

    def init_mk(self):
        super().init_mk()
        #
        self.mk.tools // '' //\
            f'{"PIP":<8} = $(BIN)/pip3' //\
            f'{"PY":<8} = $(BIN)/python3' //\
            f'{"PYT":<8} = $(BIN)/pytest' //\
            f'{"PEP":<8} = $(BIN)/autopep8 --ignore=E26,E302,E401,E402'
        #
        self.mk.all.targets // ' $(PY) $(MODULE).py'
        self.mk.all // '$^'
        self.mk.repl.targets // ' $(PY) $(MODULE).py'
        self.mk.repl // '$(PY) -i $(MODULE).py'
        self.mk.test.targets // ' $(PYT) test_$(MODULE).py'
        self.mk.test // '$^'
        # (S('.PHONY: test\ntest: $(PYT) test_$(MODULE).py', '') // '$^')
        #
        self.mk.install //\
            f'$(MAKE) $(PIP)' //\
            f'$(PIP)  install    -r {self.reqs}'
        self.mk.update //\
            f'$(PIP)  install -U    pip' //\
            f'$(PIP)  install -U -r {self.reqs}'
        self.mk.py = Section('py/install')
        self.mk.update.after(self.mk.py)
        self.mk.py //\
            '$(PIP) $(PY):' //\
            '\tpython3 -m venv .' //\
            '\t$(PIP) install -U pip pylint autopep8' //\
            '$(PYT):' //\
            '\t$(PIP) install -U pytest'
        self.mk.src // 'SRC += $(MODULE).py'
        self.mk.merge // f'MERGE += {self.reqs} $(MODULE).py test_$(MODULE).py'
        self.mk.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        settings = self.vscode.settings
        #
        settings.top // '\t"python.pythonPath":               "./bin/python3",'
        settings.top // '\t"python.formatting.provider":      "autopep8",'
        settings.top // '\t"python.formatting.autopep8Path":  "./bin/autopep8",'
        settings.top // '\t"python.formatting.autopep8Args": ["--ignore=E26,E302,E401,E402"],'
        #
        # self.f11.cmd.val = 'make repl'
        # self.f12.cmd.val = 'exit()'
        #
        files = Section('python') //\
            '"**/bin/**": true, "**/include/**":true,' //\
            '"**/lib*/**":true, "**/share/**"  :true,' //\
            '"**/*.pyc":  true, "**/pyvenv.cfg":true,' //\
            '"**/__pycache__/": true, "**/.pytest_cache/": true,'
        self.vscode.watcher // files
        self.vscode.exclude // files
        #
        self.vscode.assoc //\
            '"**/.py": "python",' //\
            '"**/requirements{/**,*}.{txt,in,pip}": "pip-requirements",'
        #
        settings.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext // '"ms-python.python",'
        self.vscode.ext.sync()

    def init_vscode_launch(self):
        super().init_vscode_launch()
        launch = self.vscode.launch
        # program
        launch.program = String(self)
        launch.django = String('false')
        launch.args = S('"args": [', '],', 0)
        launch.opts = S('//"debugOptions": [', '],', 0)
        #
        launch.it // (S('{', '}') //
                      ('"name": "Python: %s",' % self.val) //
                      '"type": "python",' //
                      '"request": "launch",' //
                      (S('"program": "', '",', 0) // launch.program) //
                      (launch.args) //
                      '"console": "integratedTerminal",' //
                      (S('"django": ', ',', 0) // launch.django)
                      )
    #     # console
    #     self.launch.mid //
    #     self.launch.mid // '\t\t}'
        launch.sync()

    def init_py(self):
        self['py'] = self.py = pyFile(self)
        self.vscode.launch.program.val = f'{self.py}'
        self.vscode.launch.sync()
        self['dir'] // self.py
        self.py.top // pyImport('config')
        return self.py.sync()

    def init_config(self):
        super().init_config()
        self.config.py = pyFile('config')
        self['dir'] // self.config.py
        self.config.py //\
            f'{"SECRET_KEY":<11} = "{self.config.secret_key}"' //\
            f'{"HOST":<11} = "{self.config.host}"' //\
            f'{"PORT":<11} = {self.config.port}' //\
            "assert PORT in range(1024,0xBFFF)"
        return self.config.py.sync()


## @ingroup py
class metalpyModule(pyModule):

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
        self.py.title = self.py['title'] = Section('title')
        self.py.metal // self.py.title
        self.py.title // "TITLE = MODULE['TITLE'] = Title(MODULE)"
        self.py.about = self.py['about'] = Section('about')
        self.py.metal // self.py.about
        # self.py.github = self.py['github'] = Section('github', comment=None)
        # self.meta // self.py.github
        self.py.readme = self.py['readme'] = Section('readme')
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
        # self.py['tail'] // Section('init')
        self.py.sync()
        # config
        config = pyFile('config')
        self.mksrc(config)
        self.diroot['config'] = config
        self.diroot // config
        # config['head'] // '## @brief site-local private config'
        # config['head'] // ''
        # config['head'] // '## @defgroup config config'
        # config['head'] // '## @brief site-local private config'
        # config['head'] // '## @{'
        # config['tail'] // '\n## @}'
        config.sync()

    def py(self):
        ret = '## @brief %s' % self.head(test=True)
        return ret

## @ingroup py
class replModule(pyModule):

    def init_py(self):
        super().init_py()
        self['test'] = self.test = pytestFile(self.py)
        self.diroot // self.test
        self.test.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.all //\
            (S(f'.PHONY: repl\nrepl: $(PY) $(MODULE).py') //
             '$(MAKE) test' //
             '$(PY) -i $(MODULE).py' //
             '$(MAKE) $@')
        self.mk.sync()

## @ingroup py
class bountyModule(pyModule):
    def __init__(self, V=None):
        pyModule.__init__(self, V)
        self.github = self['GITHUB'] = Url(
            f'https://bitbucket.org/ponyatov/{self}')
        self.github['branch'] = '/src/master/'
        self['ABOUT'] = self.ABOUT = S(
            '') // Url(f'https://bountify.co/{self}')


## @defgroup samples
## @brief samples on using `metaL` for programming and modeling

## @defgroup web web
## @brief Web Development
## @{

from html import *

class watFile(File):
    def __init__(self, V, ext='.wat', comment=';;'):
        super().__init__(V, ext, comment)

class webModule(pyModule):

    def __init__(self, V=None):
        super().__init__(V)
        self['back'] = self.back = Color('#222')
        self['fore'] = self.fore = Color('#DDD')
        self.init_static()
        self.init_templates()
        self.init_leaflet()
        # self.init_wasm()

    def init_wasm(self):
        (self.apt // 'wabt').sync()
        (self.static.giti // '*.wasm').sync()
        (self.src.giti // '*.wat.?').sync()
        self.vscode.ext.ext // '"dtsvet.vscode-wasm",'
        self.vscode.ext.sync()
        self.mk.wat = wat = Section('wat')
        self.mk.src // wat
        self.mk.wasm = wasm = Section('wasm')
        self.mk.all // wasm
        wasm // '.PHONY: wasm\nwasm: $(WAT)'
        self.mk.install // '#$(MAKE) wasm'
        self.mk.update // '#$(MAKE) wasm'
        self.mk.rules // (S('static/%.wasm: src/%.wat') //
                          'wat2wasm -v $< -o $@' //
                          'wasm2wat -v $@ -o $<.s'
                          )
        #
        self.src['hello'] = self.src.hello = hello = watFile('hello')
        self.src // self.src.hello
        wat // f'SRC += src/{hello}' // f'WAT += static/hello.wasm'
        hello.top //\
            ';; https://developer.mozilla.org/en-US/docs/WebAssembly/Understanding_the_text_format' //\
            ';; https://www.freecodecamp.org/news/get-started-with-webassembly-using-only-14-lines-of-javascript-b37b6aaca1e4/' //\
            '(module'
        hello.bot // ')'
        #
        fn_hello = S('(func', ')')
        # fn_hello // '(param i32)'
        hello.mid // fn_hello
        #
        self.src.hello.sync()

    def init_static(self):
        self['static'] = self.static = static = Dir('static')
        self.diroot // static
        static.sync()
        static.giti = giti = File('.gitignore', comment=None)
        static // giti
        giti // 'jquery.js' // 'bootstrap.*'
        giti // 'leaflet.*' // 'images/marker-*.png' // 'images/layers*.png'
        giti.sync()
        self.init_static_manifest()
        # return static

    ## https://leafletjs.com/examples/quick-start/
    def init_leaflet(self):

        css_crc = "sha512-xodZBNTC5n17Xt2atTPuE1HxjVMSvLVW9ocqUKLsCC5CXdbqCmblAshOMAS6/keqq/sMZMZ19scR4PsZChSR7A=="
        js_crc = "sha512-XQoYMqMTK8LvdxXYG3nZ448hOEQiglfqkJs1NOQV44cWnUrBc8PkAOcXy20w0vlaXaVUearIOBhiXZ5V3ynxwA=="
        self['leaflet'] = self.leaflet = leaf = Dict('leaflet')
        leaf['css'] = leaf.css = H('link', 0,
                                   rel="stylesheet", href=self.static_url("leaflet.css"),
                                   integrity=css_crc)#, crossorigin="")
        leaf['js'] = leaf.js = H('script', 1, src=self.static_url("leaflet.js"),
                                 integrity=js_crc)#, crossorigin="")
        leaf['id'] = leaf.id = f'leaf'
        leaf['div'] = leaf.div = H('div', clazz='leaflet',
                                   id=leaf.id) // f"{leaf.id}"
        leaf.sync()
        self.tmp.giti // 'leaflet.*' // 'images/marker-*' // 'images/layers*.png'
        self.tmp.giti.sync()
        self.static.css //\
            (CSS('.leaflet *', 0) //
             'background: transparent !important;')
        self.static.css //\
            (CSS('.olMap *', 0) // 'background: transparent !important;') //\
            (CSS('.olControlAttribution', 0) // 'visibility: hidden;') //\
            (CSS('.olControlScale', 0) // 'visibility: hidden;') //\
            (CSS('.olControlMousePosition', 0) // 'color:black !important;')
        self.static.css.sync()

    # ## intercept `A[key]=B` operations
    # def __setitem__(self, key, that):
    #     super().__setitem__(key, that)
    #     if isinstance(that, Title):
    #         self.init_static()

    def init_static_manifest(self):
        self.static.manifest = File('manifest', ext='', comment='')
        self.static['manifest'] = self.static.manifest
        self.static // self.static.manifest
        self.static.manifest // (S('{', '}') //
                                 f'"short_name": "{self.head(test=True)[1:-1]}",' //
                                 f'"name": "{self["TITLE"]}",' //
                                 f'"theme_color": "{self.back}",' //
                                 f'"background_color": "{self.back}",' //
                                 '"display": "standalone",' //
                                 (S('"icons": [', ']') //
                                  (S('{', '}') //
                                   '"src": "/static/logo.png",' //
                                   '"type": "image/png",' //
                                   '"sizes": "256x256"'
                                   )
                                  )
                                 )
        self.static.manifest.sync()

    def init_templates(self):
        self['templates'] = self.templates = Dir('templates')
        self.diroot // self.templates
        self.templates.sync()
        self.init_templates_css()
        self.init_templates_all()
        self.init_templates_index()

    def static_url(self, filename):
        return f'{filename}'

    def init_templates_css(self):
        self.static['css'] = self.static.css = self.css = cssFile('css')
        self.static // self.static.css
        self.static.css.print = (S('@media print {', '}') //
                                 (CSS("@page", 0) //
                                  'margin:5mm; ' // 'margin-left:30mm;') //
                                 (CSS("body", 0) //
                                  "padding:0;") //
                                 (CSS("a[href]:after", 0) //
                                  "display: none !important;")
                                 )
        self.static.css //\
            (CSS('*', 0) // f'background:{self.back} !important; color:{self.fore};') //\
            (CSS('pre', 0) // f'color:{self.fore};') //\
            (CSS("body", 0) // "padding:4mm;") //\
            (CSS('.center', 0) // 'text-align: center;') //\
            (CSS('.required', 0) // 'color:orange !important;') //\
            (CSS('a:hover', 0) // 'color:lightblue;') //\
            (CSS('label', 0) // 'color: white !important;') //\
            S('select,option,button,') //\
            (CSS('input,textarea') //
             'background-color: lightyellow !important; ' //
             'color: black !important;'
             ) //\
            (Section('print', 0) // self.static.css.print)
        # (CSS('.login', 0) // f'background:{self.back};') //\
        self.static.css.sync()

    def templates_load_static(self):
        return '{% load static %}'

    def templates_all_head(self):
        return (Section('templates_all_head') //
                '<meta charset="utf-8">' //
                '<meta http-equiv="X-UA-Compatible" content="IE=edge">' //
                '<meta name="viewport" content="width=device-width, initial-scale=1">' //
                f'<title>{{% block title %}}&lt;{self.head(test=True)[1:-1]}&gt;{{% endblock %}}</title>' //
                f'<link rel="manifest" href="{self.static_url("manifest")}">' //
                f'<link href="{self.static_url("bootstrap.css")}" rel="stylesheet">' //
                f'<link rel="shortcut icon" href="{self.static_url("logo.png")}" type="image/png">' //
                f'<link href="{self.static_url("css.css")}" rel="stylesheet">')

    def if_authenticated(self, code):
        return code

    def init_templates_all(self):
        self.templates['all'] = self.templates.all = htFile('all')
        self.templates // self.templates.all
        self.templates.all.top //\
            self.templates_load_static() //\
            '<!doctype html>'
        #
        self.templates.all.jinja = jinja = Section('jinja')
        html = H('html', lang='ru')
        html.end = ''
        self.templates.all.top // jinja // html
        # <head>
        head = H('head')
        html // head
        head // self.templates_all_head() // '{% block head %}{% endblock %}'
        # <style>
        self.templates.all.style = style = Section('style')
        hstyle = H('style')
        hstyle.comment = lambda: ''
        self.templates.all.top // (hstyle // style)
        style // '{% block style %}{% endblock %}'
        #
        body = H('body')
        self.templates.all.mid // body
        body // self.if_authenticated(S('{% block body %}',
                                        '{% endblock %}', 0))
        # body //\
        #
        #      S('{% block body %}', '{% endblock %}', 0) //
        #
        #
        self.templates.all.bot //\
            '</html>' //\
            (Section('script') //
             f'<script src="{self.static_url("jquery.js")}"></script>' //
             f'<script src="{self.static_url("bootstrap.js")}"></script>' //
             self.if_authenticated('{% block script %}{% endblock %}'))
        #  (S('{% if user.is_authenticated %}', '{% endif %}') //
        #   '{% block script %}{% endblock %}'))
        #
        return self.templates.all.sync()

    def init_templates_index(self):
        self.templates['index'] = self.templates.index = htFile('index')
        self.templates // self.templates.index
        self.templates.index.top //\
            "{% extends 'all.html' %}" //\
            self.templates_load_static()
        return self.templates.index.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        settings = self.vscode.settings
        self.vscode.assoc //\
            '"**/*.html": "html",'
        return settings.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext //\
            '"ecmel.vscode-html-css",' //\
            '"alexcvzz.vscode-sqlite",'
        return self.vscode.ext.sync()

    def init_mk(self):
        super().init_mk()
        # js
        self.mk.install // '$(MAKE) js'
        self.mk.js = Section('js/install')
        self.mk.js.static = S("js:", '', 0)
        self.mk.update.after(self.mk.js)
        self.mk.js //\
            ".PHONY: js" // (self.mk.js.static //
                             " static/jquery.js" //
                             " static/bootstrap.css static/bootstrap.js" //
                             " \\\n\tstatic/leaflet.js")
        self.mk.js // (Section('js/jquery') //
                       "JQUERY_VER = 3.5.0" //
                       (S("static/jquery.js:") //
                        "$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js"))
        self.mk.js // (Section('js/bootstrap') //
                       "BOOTSTRAP_VER = 3.4.1" //
                       "BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/" //
                       (S("static/bootstrap.css:") //
                        "$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css") //
                       (S("static/bootstrap.js:") //
                        "$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js"))
        self.mk.js // (Section('js/leaflet') //
                       "LEAFLET_VER = 1.7.1" //
                       "LEAFLET_ZIP = http://cdn.leafletjs.com/leaflet/v$(LEAFLET_VER)/leaflet.zip" //
                       (S("static/leaflet.js: $(TMP)/leaflet.zip") //
                        "unzip -d static $< leaflet.css leaflet.js* images/* && touch $@") //
                       (S("$(TMP)/leaflet.zip:") //
                        "$(WGET) -O $@ $(LEAFLET_ZIP)")
                       )
        #
        self.mk.merge // 'MERGE += static templates'
        return self.mk.sync()


rexPHONE = [r"\+7 \d{3} \d{2} \d{2} \d{3}", '+7 ??? ?? ?? ???']
rexOKATO = [r"(36|53)\d{9}", 'ОКАТО: 11 цифр']
rexKLADR = [r"(63|56)\d{11,15}", 'КЛАДР: 13..17 цифр']

#@ @}

## @defgroup html html
## @ingroup web
## @brief `HTML/CSS`
## @{

class htFile(File):
    def __init__(self, V):
        super().__init__(V, ext='.html', comment='<!--')
class cssFile(File):
    def __init__(self, V):
        super().__init__(V, ext='.css', comment='/*')

## @}

## @defgroup js js
## @ingroup web
## @brief `JavaScript`
## @{

class jsFile(File):
    def __init__(self, V):
        super().__init__(V, ext='.js', comment='//')

class jsonFile(File):
    def __init__(self, V):
        super().__init__(V, ext='.json', comment=None)

## @}


## @defgroup lexer lexer
## @ingroup parser


import ply.lex as lex

## @ingroup lexer
## token types
tokens = ['name', 'string',
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
def t_name(t):
    r'[^ \t\r\n\#\+\-\*\/\^\\(\)\[\]\{\}\:\=\.\@]+'
    t.value = Name(t.value)
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
##    ' fn : fn name bar '
def p_fn_bar(p):
    ' fn : fn name bar '
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
##    ' ex : name '
def p_ex_name(p):
    ' ex : name '
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
