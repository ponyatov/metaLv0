
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
# \ <section:top>
## @brief Distilled `metaL` / SICP chapter 4 / -- reference implementation
## https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d
# / <section:top>
# \ <section:mid>
# \ <section:Object>

class Object:
	## @name fields: metaL manifest
	## https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff#70d2d317a4fd4c95904b0a4bf46f2027
	## @{
		def __init__(self, V):
			## type/class tag
				self.tag  = self.__class__
			## scalar value: object name, string, number,..
				self.val  = V
			## slots = attributes = associative array
				self.slot = {}
			## nested AST = vector = stack = queue
				self.nest = []
			## parent nodes refset
				self.par  = set()
			## unique global storage identifier (*content* fast 32-bit hash)
				self.gid = id(self)
	## @}
	## @name dump
	## https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d#2cd65706a8b843dca6fa8c4ae69920d5
	## @{
		def __repr__(self):
			return self.dump()
		def test(self):
			return self.dump(test=True)
		def dump(self, cycle=[], depth=0, prefix='', test=False):
			ret = self.pad(depth) + self.head(prefix, test)
			for i in sorted(self.slot.keys()):
				ret += self.slot[i].dump(cycle, depth+1, prefix=f'{i} = ', test=test)
			idx = 0
			for j in self.nest:
				ret += j.dump(cycle, depth+1, prefix=f'{idx}: ', test=test)
				idx += 1
			return ret
		def head(self, prefix='', test=False):
			ret = '%s<%s:%s>' % (prefix, self._tag(), self._val())
			if not test: ret += '#%.8x @%x ' % (self.gid, id(self))
			return ret
		def pad(self, depth):
			return '\n' + '\t' * depth
		def _tag(self):
			return self.tag.__name__.lower()
		def _val(self):
			return '%s' % self.val
	## @}
	## @name operator
	## @{
		def __getitem__(self, key):
			if isinstance(key,str):
				return self.slot[key]
			if isinstance(key,int):
				return self.nest[key]
			raise TypeError(key)
		def __floordiv__(self, that):
			self.nest.append(that)
			return self
	## @}
	## @name evaluation
	## @{
		def eval(self, ctx):
			raise NotImplementedError
		def apply(self, that, ctx):
			raise NotImplementedError
	## @}

class Nil(Object): pass

class Error(Object): pass
# / <section:Object>
# \ <section:Primitive>

class Primitive(Object):
	def eval(self, ctx):
		return self

class Symbol(Primitive):
	def eval(self, ctx):
		return ctx[self.val]

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
# \ <section:Context>

class Context(Active): pass

glob = Context('global')

# / <section:Context>

class Fn(Active): pass

class Op(Active): pass
# / <section:Active>
# \ <section:Meta>

class Meta(Object): pass

class Module(Meta): pass

class Class(Meta): pass

class Method(Meta,Fn): pass

class Args(Meta,Vector): pass
# / <section:Meta>
# \ <section:IO>

class IO(Object): pass

class Dir(IO): pass

class File(IO): pass
# / <section:IO>
# / <section:mid>