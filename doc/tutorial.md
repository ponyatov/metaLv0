# Tutorial {#tutorial}

see also <a href=modules.html>modules</a> and <a href=index.html>main page</a> (README.md)

***

The `metaL` (meta)programming language was designed as a mix of Lisp and Python,
not of syntax, but to get feels of language abilities.

* *Python* is simple to use and have very friendly syntax
* *Lisp* has a power of self-modification able to change program in runtime
* *Smalltalk* is pure OOP-language works over message passing which is good for
  distributed and parallel systems

`metaL` **targets** not on writing application programs, but **on writing
programs that generate other programs** (into C code which can be compiled and
run on any computer system).

Don't try to write something which must be fast like number crunching or game
engine -- `metaL` just does not work like that, and was not designed to be fast.
It was created for manipulations with program structures, and you can write
extra fast programs in `metaL` if you use it a wright way: for source code
generation of your application.

***

### system startup

* installation
```sh
~$ git clone -o gh https://github.com/ponyatov/metaL
~$ cd metaL
~/metaL$ make install
```
* interactive with @ref REPL() autorun
```sh
~/metaL$ make metaL/repl
```
* in Python-only mode: press [Ctrl]+[C] to exit into Pyhon interactive console
```
/home/ponyatov/metaL/bin/python3 -i metaL.py

<vm:metaL> #14ee5988 @7f12f298b128
        ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7f12f298b5f8

<vm:metaL> Ctrl+C

Traceback (most recent call last):
  File "metaL.py", line 1246, in <module>
    REPL()
  File "metaL.py", line 1228, in REPL
    command = input(vm.head(test=True) + ' ')
KeyboardInterrupt
>>> print('Python')
Python
>>>
```

### `metaL` DDL/DML script

* **only single line syntax** can be used for every command /Python `input()`
  limitation in @ref REPL() /
* can be run in Python mode as string via function @ref metaL()
```py
comment = ' # line comment '
metaL(comment)
```
```py
integer = ' -01 # integer '
metaL(integer)
```
* can be interactively executed after @ref REPL() start

Recommended use is running under any IDE can send selected code from a text
editor to running terminal session with active REPL. After all code were tested
in an interactive shell, it can be saved, and system should be restarted for
changes commit.

### Literals

Some set of language elements can be inputted directly, which are called
literals. They are numbers, strings, and symbols.

* numbers
```py
number = ' +02.30 # floating point '
metaL(number)
```
```py
integer = ' -01 # integer '
metaL(integer)
```
```py
ihex = ' 0xDeadBeef # hexadecimal '
metaL(ihex)
```
```py
ibin = ' 0b1101 # binary '
metaL(ibin)
```

* strings
```py
simple = " 'single line\n\twith escaped chars' "
metaL(simple)
```
Multiline strings can be parsed, but it is not an exception from the
single-lined syntax, as REPL can't correctly input such strings. The only way to
input them is by using `metaL()` in Python mode.
```py
multiline = """ 'multiple lines
\twith escaped chars'
"""
metaL(multiline)
```

* symbols: any none-space char groups
```py
symbol = 'MODULE'
metaL(symbol)
```
The `Symbol` type differs from other literals: most of them evaluate to itself,
but **symbols will do a lookup in current computation context** as a variable
name in other programming languages.
```
<vm:metaL> MODULE

<symbol:MODULE> #8b2b5473 @7f54949d8048

<module:metaL> #d80c934b @7f5494ffab38

<vm:metaL> #14ee5988 @7f5494ffa710
        ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7f5494ffabe0
------------------------------------------------------------------
<vm:metaL>
```

### REPL cycle

Read-Eval-Print-Loop runs in three stages after every line in the source code
string were split by new line chars (besides multiline strings):
```py
>>> metaL(' -01 \n +2.30 ')

  <ast:>
    <op:-> #f70b8dac @7f01078ac080
      0: <integer:1> #47696a48 @7f01078ac1d0
    <op:+> #63257116 @7f01078ac320
      0: <number:2.3> #c4287bc0 @7f01078ac400
```
1. pure parsing: every line will be parsed into an AST (Abstract Syntax Tree)
   combined from the `metaL` objects
   ```
      <op:-> #f70b8dac @7f01078ac080
         0: <integer:1> #47696a48 @7f01078ac1d0
   ```
2. evaluation: `metaL` objects composite structure runs via `eval`/`apply`
   methods
   ```
      <integer:-1> #d85c1811 @7f905edd3e10
   ```
3. When you run `metaL` scripts via an interactive shell, every line will be
   printed as parsed-only AST and evaluated object, followed by the current VM
   state.
   ```
      <vm:metaL> #14ee5988 @7fc7328d7828
         ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7fc7328d7cf8
         ...
         vm = <vm:metaL> #14ee5988 @7fc7328d7828 _/
   ```
