
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
import config
# / <section:top>
# \ <section:mid>
# \ <section:refset>
## set of references to objects
class refset: pass
# / <section:refset>
# \ <section:Object>

class Object:
	tag = "object"

	## @name fields: metaL manifest
	## https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff#70d2d317a4fd4c95904b0a4bf46f2027
	## @{

	def __init__(self, V):
		## type/class tag
		self.tag  = self.__class__.tag
		## scalar value: object name, string, number,..
		self.val  = V
		## slots = attributes = associative array = env (var bindings)
		self.slot = {}
		## nested AST = vector = stack = queue = any ordered container
		self.nest = []
		## parent nodes references
		self.par  = refset()
		## unique global storage identifier (fast 32-bit hash over *content*)
		self.gid  = id(self) # self.sync() | [xx]hash(self)

	## @}

	## @name dump
	## https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d#2cd65706a8b843dca6fa8c4ae69920d5
	## @{

	## system method dumps any object in a string form
	def __repr__(self):
		return self.dump()

	## method used in `test_distill.py` dumps wihout `#hash`/`@id`
	def test(self):
		return self.dump(test=True)

	## full text-tree dump
	def dump(self, cycle=[], depth=0, prefix='', test=False):
		# `<T:V>` header
		ret = self.pad(depth) + self.head(prefix, test)
		# block infinite cycles
		if not depth: cycle=[] # recursion init
		if self in cycle: return f'{ret} _/'
		cycle.append(self)
		# slot{}s
		for i in sorted(self.slot.keys()):
			ret += self.slot[i].dump(cycle, depth+1, f'{i} = ', test)
		# nest[]ed
		for j, k in enumerate(self.nest):
			ret += k.dump(cycle, depth+1, f'{j}: ', test)
		#
		return ret

	## short `<T:V>` header only
	def head(self, prefix='', test=False):
		ret = '%s<%s:%s>' % (prefix, self.tag, self._val())
		if not test: ret += f' #{self.gid:<8x} @{id(self)}'
		return ret

	## dump tree padding
	def pad(self, depth):
		return '\n' + '\t' * depth

	## `.val`-formatter for dumps
	def _val(self):
		return '%s' % self.val

	## @}

	## @name operator
	## @{

	## `A[key]`
	def __getitem__(self, key):
		if isinstance(key,str):
			return self.slot[key]
		if isinstance(key,int):
			return self.nest[key]
		raise TypeError(key)

	## `A[key] = B`
	def __setitem__(self, key, that): pass

	## `A // B -> A.push(B)`
	def __floordiv__(self, that):
		self.nest.append(that)
		return self

	## @}

	## @name evaluation
	## @{

	## evaluate in context
	def eval(self, ctx):
		raise NotImplementedError

	## apply to object in context
	def apply(self, that, ctx):
		raise NotImplementedError

	## @}

class Nil(Object): pass

class Error(Object): pass
# / <section:Object>
# \ <section:Primitive>
class Primitive(Object): pass
class Symbol(Primitive): pass
class String(Primitive): pass
class Number(Primitive): pass
class Integer(Primitive): pass
# / <section:Primitive>
# \ <section:Container>
class Container(Object): pass
class Vector(Container): pass
class Stack(Container): pass
class Dict(Container): pass
class Set(Container): pass
class Queue(Container): pass
# / <section:Container>
# \ <section:Active>
class Active(Object): pass
class Context(Active): pass
class Fn(Active): pass
class Op(Active): pass
# / <section:Active>
# \ <section:Meta>
class Meta(Object): pass
class Module(Meta): pass
class Class(Meta): pass
class Method(Meta, Fn): pass
class Args(Meta, Vector): pass
# / <section:Meta>
# \ <section:IO>
class IO(Object): pass
class Dir(IO): pass
class File(IO): pass
# / <section:IO>
# / <section:mid>