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
        assert lexer.token() != None # nl

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

    def test_vector_multy(self):
        multy = parser.parse('[1,2.3,MODULE]')
        assert multy.test() ==\
            '\n<ast:>\n\t0: <vector:>' +\
            '\n\t\t0: <integer:1>' +\
            '\n\t\t1: <number:2.3>' +\
            '\n\t\t2: <symbol:MODULE>'
        assert multy.eval(vm).test() ==\
            '\n<ast:>\n\t0: <vector:>' +\
            '\n\t\t0: <integer:1>' +\
            '\n\t\t1: <number:2.3>' +\
            '\n\t\t2: <module:metaL>'

    def test_numbers(self):
        ast = parser.parse('''
            # numbers
            [ -01 , +02.30 , -4e+5 , +6.7e-8 , 0xDeadBeef , 0b1101 ]
            ''')
        # ast
        assert ast.test() ==\
            '\n<ast:>\n\t0: <vector:>' +\
            '\n\t\t0: <op:->\n\t\t\t0: <integer:1>' +\
            '\n\t\t1: <op:+>\n\t\t\t0: <number:2.3>' +\
            '\n\t\t2: <op:->\n\t\t\t0: <number:400000.0>' +\
            '\n\t\t3: <op:+>\n\t\t\t0: <number:6.7e-08>' +\
            '\n\t\t4: <hex:0xdeadbeef>' +\
            '\n\t\t5: <bin:0b1101>'
        # evaled
        assert ast.eval(vm).test() ==\
            '\n<ast:>\n\t0: <vector:>' +\
            '\n\t\t0: <integer:-1>' +\
            '\n\t\t1: <number:2.3>' +\
            '\n\t\t2: <number:-400000.0>' +\
            '\n\t\t3: <number:6.7e-08>' +\
            '\n\t\t4: <hex:0xdeadbeef>' +\
            '\n\t\t5: <bin:0b1101>'

class TestIntMath():

    def test_plus(self):
        ast = parser.parse('+486')[0]
        assert ast.test() ==\
            '\n<op:+>' +\
            '\n\t0: <integer:486>'
        assert ast.eval(vm).test() ==\
            '\n<integer:486>'

    def test_minus(self):
        ast = parser.parse('- 486')[0] # spaces allowed
        assert ast.test() ==\
            '\n<op:->' +\
            '\n\t0: <integer:486>'
        assert ast.eval(vm).test() ==\
            '\n<integer:-486>'

    def test_add(self):
        ast = parser.parse('137+349')[0]
        assert ast.test() ==\
            '\n<op:+>' +\
            '\n\t0: <integer:137>' +\
            '\n\t1: <integer:349>'
        assert ast.eval(vm).test() ==\
            '\n<integer:486>'

    def test_sub(self):
        ast = parser.parse('1000-334')[0]
        assert ast.test() ==\
            '\n<op:->' +\
            '\n\t0: <integer:1000>' +\
            '\n\t1: <integer:334>'
        assert ast.eval(vm).test() ==\
            '\n<integer:666>'

    def test_mul(self):
        ast = parser.parse('5*99')[0]
        assert ast.test() ==\
            '\n<op:*>' +\
            '\n\t0: <integer:5>' +\
            '\n\t1: <integer:99>'
        assert ast.eval(vm).test() ==\
            '\n<integer:495>'

    def test_div(self):
        ast = parser.parse('10/5')[0]
        assert ast.test() ==\
            '\n<op:/>' +\
            '\n\t0: <integer:10>' +\
            '\n\t1: <integer:5>'
        assert ast.eval(vm).test() ==\
            '\n<integer:2>'

## @ref parser
## @ingroup test
class TestFn:

    def test_empty(self):
        ast = parser.parse('{}')
        assert ast.test() == \
            '\n<ast:>' +\
            '\n\t0: <fn:>' +\
            '\n\t\targs = <args:>' +\
            '\n\t\tret = <nil:>'

    def test_single(self):
        ast = parser.parse('{123}')
        assert ast.test() == \
            '\n<ast:>' +\
            '\n\t0: <fn:>' +\
            '\n\t\targs = <args:>' +\
            '\n\t\tret = <nil:>' +\
            '\n\t\t0: <integer:123>'
