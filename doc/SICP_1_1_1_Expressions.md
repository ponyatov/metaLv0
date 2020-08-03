# SICP 1.1.1 Expressions

https://xuanji.appspot.com/isicp/1-1-elements.html

Numerical constant in Lisp/Scheme

```lisp
lisp> 486
486
```

is equal to `metaL` object in Python:

```py
>>> Integer(486)

<integer:486> @7fd3b22280f0
```

and also in `metaL` CLI shell:

```
metaL> 486

# AST parsed from DML/DDL line
<integer:486> @7f0f7c52a358

# evaluated AST
<integer:486> @7f0f7c52a358
------------------------------------------------------------------
```

Differences of `metaL` language model from generic Lisp/Scheme described in the [SICP] book:
* lists are totally replaced by object graphs, every element is typed, which is
  closer to [Prolog predicate structures](http://wambook.sourceforge.net/) then
  Lisp lists/trees
* there are no atoms -- every `Primitive` object can have arbitrary attributes and
  even nested subelements (such as units or tolerance data)
* there is a special case of `Op`erators which has a fixed number of operands
  and can't be applied such a `+` function here:

### `(+ 137 349)`

```lisp
> (+ 137 349)
486
```
```py
>>> ast = Op('+') // Integer(137) // Integer(349)
>>> ast

<op:+> @7f0f8aad2208
        0: <integer:137> @7f0f8aad2240
        1: <integer:349> @7f0f8aad2828

>>> ast.eval(vm)

<integer:486> @7fd06e7c7828
```
```
metaL> 137+439

<op:+> @7f0b0065c6a0
        0: <integer:137> @7f0b0065c588
        1: <integer:439> @7f0b0065c8d0

<integer:576> @7f0b0065c1d0
------------------------------------------------------------------
```

### `(- 1000 334)`

```lisp
> (- 1000 334)
666
```
```py
>>> ast = Op('-') // Integer(1000) // Integer(334)
>>> ast

<op:-> @7f535f2c91d0
        0: <integer:1000> @7f535f2c9208
        1: <integer:334> @7f535f2c9240

>>> ast.eval(vm)

<integer:666> @7f535f2c9278
```
```
metaL> 1000 -334

<op:-> @7fe5164426a0
        0: <integer:1000> @7fe516442898
        1: <integer:334> @7fe5164428d0

<integer:666> @7fe5164421d0
------------------------------------------------------------------
```

### `(* 5 99)`

```lisp
> (* 5 99)
495
```
```py
>>> parser.parse('5*99')

<ast:> @7fca95730320
        0: <op:*> @7fca95730a58
                0: <integer:5> @7fca957302e8
                1: <integer:99> @7fca95ab5080

>>> parser.parse('5*99')[0].eval(vm)

<integer:495> @7fca95ab50f0
```

The computation process is going from the parsed AST tree via:
* source code string passed to `parser.parse(source)`
* the [PLY library](https://www.dabeaz.com/ply/ply.html) provides a simple way for defining custom syntax
  * https://riptutorial.com/python/example/31583/the--hello--world---of-ply---a-simple-calculator
  * parser is an optional part of the `metaL`, and you are also free to make a syntax you want
  * if you want, you can define structures directly in Python using object graph
    constructors and special operators such as `//`, `<<`, `>>`, `object[key]`,
    and `object[key]=other`
* most complex structures can't be defined via a parser, so there only two ways leaves:
  * define structure procedurally in Python
  * use *structure self-modification*, when more simple parsed **structures must
    be executed by calling its self-interpreting methods**
    * mostly `.eval()` and `.apply()`
    * but also they have some operator and transformations methods
    * also, **you can define your own arbitrary transformation methods** for custom cases in the *host language* (Python) -- that's how `metaL` powers
    * while structure interprets itself, it can modify the context in which it is executing -- this is not pure functional but is practical in real

### `(/ 10 5)`

```lisp
> (/ 10 5)
2
```
```py
>>> parser.parse('10/5')[0].eval(vm)

<integer:2> @7f63ddb192b0
```

### `(+ 2.7 10)`

```lisp
> (+ 2.7 10)
12.7
```
```py
>>> ast = Op('+') // Number(2.7) // Integer(10)

<op:+> @7f79ea4971d0
        0: <number:2.7> @7f79ea497208
        1: <integer:10> @7f79ea497240

>>> ast.eval(vm)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "metaL.py", line 278, in eval
    return greedy[0].add(greedy[1], ctx)
  File "metaL.py", line 183, in add
    assert type(that) == self.__class__
AssertionError
```

In Lisp, we have *implicit/automatic type conversion*, so this mixed-typed
expression can be evaluated as is.

In `metaL` more rigid type checking were used to get fewer errors, and force
programmers to use an *explicit type cast* only in places where it is required.
As a result, any mixed-typed expression can be defined but will be evaluated
with an error exception.

Rigid typing is controversial especially if you mostly use Python which has a
lighter type checking.

### `(+ 21 35 12 7)`

```lisp
> (+ 21 35 12 7)
75
> (* 25 4 12)
1200
```

Lisp has unlimited numbers of operands for such functions as `+`. It can be a
bit discouraging that `metaL` operators has fixed number of operands. While I
still have no cases where it was required to support, it leaves that way, but
you can modify operator transformations to provide more compatible computation
(maybe you are porting some old Lisp software).

### `(+ (* 3 5) (- 10 6))`

```lisp
> (+ (* 3 5) (- 10 6))
19
```
```py
>>> ast = parser.parse('(+ (* 3 5) (- 10 6))')[0]
```
