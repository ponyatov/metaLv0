
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
# \ <section:top>
import pytest
def test_none(): pass
# / <section:top>
# \ <section:mid>
from metaL import *
# / <section:mid>
hello = Object('hello')
world = Object('world')
## for <pyinterface:fields: metaL manifest>
def test_hello():
	assert hello.test() == '\n<object:hello>'
	assert world.test() == '\n<object:world>'
	hello // world
	print(hello.test())
	assert hello.test() ==\
		'\n<object:hello>' +\
		'\n\t0: <object:world>'
	