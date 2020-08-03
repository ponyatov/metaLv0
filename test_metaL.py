## @file
## @brief `metaL` core test bundle

## @defgroup test tests

import pytest

from metaL import *


## @ref object
## @ingroup test
class TestObject:

    def hello(self): return Object('Hello')
    def world(self): return Object('World')

    def test_hello(self):
        assert self.hello().test() ==\
            '\n<object:Hello>'

    def test_world(self):
        assert (self.hello() // self.world()).test() ==\
            '\n<object:Hello>' +\
            '\n\t0: <object:World>'

    def test_leftright(self):
        hello = self.hello()
        world = self.world()
        left = Object('left')
        right = Object('right')
        assert (hello // world << left >> right).test() ==\
            '\n<object:Hello>' +\
            '\n\tobject = <object:left>' +\
            '\n\tright = <object:right>' +\
            '\n\t0: <object:World>'


## @ref prim
## @ingroup test
class TestPrimitive:

    def test_number(self):
        assert Number(486).test() ==\
            '\n<number:486.0>'

    def test_integer(self):
        assert Integer('-01').test() ==\
            '\n<integer:-1>'

    def test_number_dot(self):
        assert Number('+02.30').test() ==\
            '\n<number:2.3>'

    def test_hex(self):
        x = Hex('0xDeadBeef')
        assert x.test() == '\n<hex:0xdeadbeef>'
        assert x.val == 3735928559

    def test_bin(self):
        x = Bin('0b1101')
        assert x.test() == '\n<bin:0b1101>'
        assert x.val == 13


## @ref lexer
## @ingroup test
class TestLexer:

    def test_none(self):
        lexer.input('')
        assert lexer.token() == None

    def test_comment(self):
        lexer.input('# comment')
        assert lexer.token() == None

    def test_spaces(self):
        lexer.input(' \t\r\n')
        assert lexer.token() == None

    def test_symbol(self):
        lexer.input('symbol')
        token = lexer.token()
        assert token and token.value.test() ==\
            '\n<symbol:symbol>'


## @ref parser
## @ingroup test
class TestParser:

    def test_none(self):
        assert parser.parse('').test() ==\
            '\n<ast:>'

    def test_symbol(self):
        ast = parser.parse('MODULE')
        assert ast.test() ==\
            '\n<ast:>\n\t0: <symbol:MODULE>'
        assert ast.eval(vm).test() ==\
            '\n<ast:>\n\t0: <module:metaL>'

    def test_vector_empty(self):
        empty = parser.parse('[]')
        assert empty.test() ==\
            '\n<ast:>\n\t0: <vector:>'
        assert empty.eval(vm).test() ==\
            '\n<ast:>\n\t0: <vector:>'

    def test_vector_single(self):
        single = parser.parse('[MODULE]')
        assert single.test() ==\
            '\n<ast:>' +\
            '\n\t0: <vector:>' +\
            '\n\t\t0: <symbol:MODULE>'
        assert single.eval(vm).test() ==\
            '\n<ast:>' +\
            '\n\t0: <vector:>' +\
            '\n\t\t0: <module:metaL>'

