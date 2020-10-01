
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
import pytest
def test_none(): pass

from distill import *
# / <section:top>

hello = Object('hello')
world = Object('world')

def test_hello():
	assert hello.test() == '\n<object:hello>'
	assert world.test() == '\n<object:world>'
	hello // world
	print(hello.test())
	assert hello.test() ==\
		'\n<object:hello>' +\
		'\n\t0: <object:world>'
