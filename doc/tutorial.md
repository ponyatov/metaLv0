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
