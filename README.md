#  ![logo](static/logo.png) `metaL`
## Homoiconic [meta]programming [L]anguage/[L]ayer

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

* `github`: https://github.com/ponyatov/metaL
* Discord: https://discord.gg/5CYZdt6
* [book drafts](https://www.notion.so/metalang/Wiki-18ae2c8192bd4b5c8548bf7f56f390d6) en/ru
  * [`metaL` manifest](https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff)
  * [Distilled `metaL`](https://www.notion.so/metalang/Distilled-metaL-SICP-chapter-4-237378d385024f899e5a24597da7a19d)
  * [глава 4 Металингвистическая абстракция](https://www.notion.so/metalang/4-eb7dfcf3dbb04e6eb8015337af850aab)
    (частичный перевод с адаптацией)
* `doxygen` manual: https://ponyatov.github.io/metaL
  * tutorial: https://ponyatov.github.io/metaL/tutorial.html
* [version for Repl.it Language Jam contest](https://repl.it/@metaLmasters/metaL)
  * https://blog.repl.it/langjam
  * https://repl.it/talk/share/metaL-for-replit-Language-Jam-contest/46470
* [LinkedIn post](https://www.linkedin.com/pulse/how-hard-develop-your-own-programming-language-worth-dmitry-ponyatov/)
* [old repository](https://github.com/ponyatov/metaLold)

## Language Ideas Promo

* take Lisp homoiconic nature and port it to CPython3 stack (VM & libs)
* provide a light environment for **metaprogramming by code generation**
  * `metaL` is a special language for writing programs that write other programs (in C & Python as *target languages*)
  * interactive REPL with pushing generated code into files is a primary method of work
  * system bootstrap via @ref circ redefinition 
* protect people from the parens soup by using infix syntax
  and AST-friendly data structure in place of classic lists
* integrate best features from Python, Lisp/Clojure, and Smalltalk
* targets on IoT programming:
  * server-side @ref dja in Python/Django/PostgreSQL (todo: highly optimized C/C++/Rust? code)
  * ANSI C code generation is required by design
    * uses amazing [TCC](https://bellard.org/tcc/) host compiler backend for fast debug
  * cross-compiling to many embedded devices including
    AVR8, Cortex-M, and MSP430 microcontrollers
    * uses GCC cross-compiler for portability

## `metaL` is not a programming language

`metaL` **is a method of programming** in Python (or any other language you prefer: JS, PHP,...)

`metaL` works over two key features:
* homoiconic self-modifying data structures
* metaprogramming via code generation

That's why DML/DDL syntax parser is not required and is the only an optional
feature: parser was left there just to be a demo of the third magic feature of
the `metaL`:
* custom user-defined syntax

All `metaL` structures can be defined directly in the *host language* (Python),
the syntax parser is only a way to do it more simplified and to work in
symbiosis with Python REPL + VSCode. VSCode has the ability to send selected
parts of code from a text editor to a terminal with running REPL. This sending
has some disadvantage: Python's `input()` function can input only a single
string, so when we send a text from a VSCode, we can't detect was it a single
line or multiple lines text block. So, the syntax was chosen single-lined. It
also points, that DML/DDL in `metaL` is not a programming language, it's a
language of CLI commands.

As we can use code generation for producing transformations in a host language,
*it is possible to leave `metaL` without user-defined functions* and
continuations, which are complex to understand and implement for the newbie
language designer. User function (method, new user type class) can be specified,
translated into host language without its execution, resulting code should be
pasted into `metaL.py`, and finally system restarts with this new working
transformation. As `metaL` were primarily designed for work with interactive
code generation, such system redefinition method is suitable for use, especially
if we'll have `metaL`
[metacircular implementation](https://stackoverflow.com/questions/1481053/what-is-the-exact-definition-of-a-metacircular-interpreter)
in the system release.

### Generic Code Templating

The idea of `metaL` originates from an idea of the *generic code templating*:
any mainstream programming language we're using any day at work or for a hobby
is limited by its vendors, the huge community which uses it, and a language
stack of tools and libraries. Even if you have enough skills to take something
like CPython implementation and hack it to add some language modifications you
want, you never can use it in production -- these mods make the language
incompatible with the generic branch, and the most important it makes your team
developers incompatible with the rest of community. If you try to use your own
hacked Python or some homebrewed language for work, you will be kicked by your
employer and team as it introduces risk in hiring new developers, adds vendor
lock on uncommon language and tools, and dissipates efforts also on custom
language support.

The idea about code templating is a way of taking the power of custom
highest-level language still having no incompatibles with your production team.
In most cases, nobody locks you on the IDE you use for development, so if you
also add some shadow tool that generates human-readable code in the mainstream
language of your team, you'll have a chance to take the power without risks
shown above.

The problem is how can we make some language especially designed to be such a
magic wand. First of all, it must be very flexible and dynamic, and at the same
time it must not be effective and fast in terms of computation, it should be
just fast enough and not more. Next, it is required that this language must have
the highest extensibility to let you describe and implement any method or
approach of programming you desire. Lisp language dialects are well known at
this position, but they have scary syntax and at the same time are well-known as
esoteric. So, to make such a magic language, we can take the Lisp dynamic
nature, implement its runtime in any language you prefer (Python), cover it with
infix syntax parser which can be extended by a user as he wants, and finally
focus on making jigs and features suitable for describing software systems at
the highest level and simplifying of code generation.

The reverse path is the legacy code analysis from source code to high-level
models. There is a common problem of moving some old software systems to a new
language stack with fixing a lot of architecture bugs. I can't remember any
freeware tool or system which able to provide an environment for sucking in
source code in arbitrary (ancient) languages, which can provide a handy way for
reverse engineering, making software models, detecting used algorithms and
methods, and regenerating software from these refurbished models.

### Concept Programming

CP here is a programming model described in the works of Enn Heraldovich Tyugu
about model-based software development. It is not mean the term by Alexsandr
Stepanov here. The common idea is about making domain models describe the
problem in a wide in the form of relation networks, and automatic program (code)
synthesis from specifications to solve concrete tasks. This synthesis works over
these networks using them as *generic knowledge representation*.

* http://www.cs.ioc.ee/~tyugu/
* J. Symbolic Computation (1988) 5, 359-375\ The Programming System PRIZ [sym88]

## Base Node Class

The core of the **graph interpreter system** is a homoiconic model uses a
directed graph of objects as both program and data representation. The idea was
taken from [minsky] and extended with the ability to store not only slots
(attributes) but also hold any knowledge frames in an ordered container.

https://www.youtube.com/watch?v=nXJ_2uGWM-M

Frames originated as a technology used for knowledge representation in
artificial intelligence. They are very close to objects and class hierarchies in
object-oriented languages although their fundamental design goals are different.
Frames are focused on the explicit and intuitive representation of knowledge
whereas objects focus on encapsulation and binding data with processing
procedures. Original Marvin Minsky's concept *lacks some principal features for
software design*, so it must be extended with the ability to *store sequential
collections*.

In practice, the techniques and capabilities of the frame model and
object-oriented languages overlap significantly so much as we can treat frames
not only a native superset of OOP but they drastically extend object design
concepts wider: we can represent any knowledge in frames, and use any
programming paradigms as we desire.

```py
class Frame:
    def __init__(self, V):
        # scalar data value
        # mostly names the frame, but also can store things like numbers and strings
        self.val = V
        # named slots = attributes = string-keyed associative array
        self.slot = {}
        # ordered storage = program AST nested elemens = vector = stack
        self.nest = []
        # unique storage id (Redis,RDBMS,..)
        self.gid = '@%x' % id(self)
```

This data node structure which combines named slots with the ordered collection
is definitively required for representing any program source code, as this is
very close to classical AST and attribute grammar but uses graph in place of the
attributed tree. The object graph (frame) representation of a program as a
primary form is effective and *native for any work involved with source code
transformations*: synthesis, modifications, analysis, cross-language
translation, etc.

Factically, **we don't require any text programming language at all**, as this
*Executable Data Structure* can

* hold any program statically (as storage),
* be executed by the EDS-interpreter, so it is *active* data
* can be translated into any mainstream programming language or
* [cross-]compiled into machine code via LLVM.

### Homoiconic programming model

**Homoiconicity** is a property of a programming language in which any program
is *simultaneously*

* an easy to modify *data structure*, and
* an *executable program representation* (program source code).

In a homoiconic language, a programmer does not just have access to the source
code, but the language itself specifically provides tools and easy to use
methods for convenient work with parts of programs (represented as generic data)
in runtime.

* Say, if you include source code of your program in C++ into the distribution
  package, you can work with the program code as data, but only at the level of
  text files, or using third-party analysis libraries. In the C++ language
  itself, there are no dedicated tools for reading, modifying, or generating
  source code.
* Conversely, in the Lisp language, all programs are represented in the form of
  executable lists -- these lists are simultaneously a program and the usual
  universal data structure for working with which the language was specially
  created.

### EDS Interpreter

In order to use the advantages of homoiconicity in your programs written in any
conventional languages (C++, Java,..), you need to integrate an
**EDS-interpreter** into your programs that will

* *execute some data structure as a program*, and additionally
* provides high-level tools for modifying program/data graph in runtime.

It is not necessary that this interpreter should include a parser of some
scripting language, as *graph structure can be generated directly by code in the
implementation language*, and by structure self-transformation. To create a
program in such a system, you only need to have any way to create an *executable
data structure* in memory: it can be GUI-based drawing, text format parser,
external graph database, or some C++ code that forces the compiler to include
such a structure in the executable file statically.

### `metaL` is no-syntax language

In a long long time, CLI (command-line interface) and scripting show itself very
effective from the first days of computing and don't go to become obsolete. So,
it is handy to have some lite DDL/DML script language in front of your
metaL-based system just to be able to use it for initialization files, and
making some interactive queries to the running system. *This DDL/DML is not the
`metaL` itself*, its just a way to host system snapshot in git-friendly text
files and provide very light CLI. But, `metaL` is the language of live data
structures in running computer memory. It specifies common ides
* how these structures are presented (unified storage),
* methods of computation (some sort of expression evaluation, close to AST
  interpretation), and
* set of node types described in the language core, which you can expand next as
  you want.

### Metaprogramming

Metaprogramming -- when one program modifies (generates) another program,
including itself.

Metaprogramming is a method of boosting your efficiency as a programmer by
expanding the language you use. If you write very similar code every day, in
languages ​​that can do meta (Lisp, Nim), you can write small macro programs
that will run during the compilation stage, and generate new code by a template,
or modify an existing code the way as you need it. Factically, you can add to
the language those features that are needed for a narrow set of your specific
tasks.

In order to be able to use metaprogramming in a full scale, the language or
programming system you are using must be homoiconic. If you want to use this
method with industrial programming languages, the use of an EDS interpreter will
allow you to quickly and conveniently solve your problems, paying for it with
some losses in the speed of programs and memory usage (see a comparison of
interpreters vs the compilers into machine code).

## Links

[SICP] [**Structure and Interpretation of Computer Programs**](https://mitpress.mit.edu/sites/default/files/sicp/full-text/book/book-Z-H-4.html#%_toc_start)
       Harold Abelson, Gerald Jay Sussman, Julie Sussman // MIT Press, 1996, ISBN	0-262-51087-1

[iSICP] [interactive SICP](https://xuanji.appspot.com/isicp)

[plai] Shriram Krishnamurthi [Programming Languages: Application and Interpretation](https://www.plai.org)

[papl] Joe Politz, Ben Lerner [Programming and Programming Languages](https://papl.cs.brown.edu/2020/)

[minsky] Marvin Minsky [**A Framework for Representing Knowledge**](https://web.media.mit.edu/~minsky/papers/Frames/frames.html)
// MIT-AI Laboratory Memo 306, June, 1974. Reprinted in The Psychology of Computer Vision, P. Winston (Ed.), McGraw-Hill, 1975.

[tyugu] **Knowledge-Based Programming** Enn Tyugu 1988 // Addison-Wesley Longman Publishing Co., Inc.

[tyuguru] Э.Х.Тыугу **Концептуальное программирование**. М.: Наука, 1984. 255 с

[sym88] J. Symbolic Computation (1988) 5, 359-375\
[**The Programming System PRIZ**](https://www.academia.edu/18315153/The_programming_system_PRIZ?auto=download)
\ G.Mints, E.Tyugu, Institute of Cybernetics, Estonian Academy of
Sciences,Tallinn 200108, USSR

[priz] **Инструментальная система программирования ЕС ЭВМ (ПРИЗ)** / М.И. Кахро,
А.П. Калья, Энн Харальдович Тыугу . – Изд. 2-е – Москва : Финансы и статистика,
1988 . – 181 с ISBN 5-279-00111-2

[actor] Hewitt, Meijer and Szyperski
[The Actor Model (everything you wanted to know...)](https://www.youtube.com/watch?v=7erJ1DV_Tlo)

### UnisonWeb

`metaL` grabs a great idea about immutable, homoiconic, and distributed data
structures from the `Unison` language. It is also important to note the method
of building the distributed knowledge database using incremental computation of
data elements.

* **The Unison language** https://www.unisonweb.org
  * Paul Chiusano [Unison: a new distributed programming language](https://www.youtube.com/watch?v=gCWtkvDQ2ZI) Strange Loop '19
  * [Unison: An Introduction and Q&A with Rúnar Bjarnason](https://www.youtube.com/watch?v=yicXcdLI2YA)

### Literate Programming

Literate Programming concept targets on mixing code with documentation, but
shows the original method is not alive due to limits forced by sequential code.
Most programming languages are sequential by its nature, so original `cweb`
forces you to write manual in order of your code, starting from `include` etc.
Disjoining code from documentation elements allows doing arbitrary structure of
the manual, and include parts of code as interactive elements.

* https://en.wikipedia.org/wiki/Literate_programming
* [Roam Athens Research](https://roamresearch.com)
  * https://www.notion.so/MVP-Update-Funding-and-Why-I-Started-Athens-e68822f0c3654660ae621cdcbf932bc4
    * https://github.com/athensresearch/athens

### Smalltalk language and pure OOP

`metaL` does not follow the Smalltalk language semantics, and especially its
strange syntax, but it looks very closely on its message-passing computation
model, especially in terms of async messaging in the [actor] model. To
understand the nature and the power of Smalltalk without the need of installing
or learning it you can see two next intro videos; don't skip a few firsts in
[lawson] playlist where you can see the magic of Smalltalk's interactive
debugging and persistent memory.

[lawson] https://www.youtube.com/playlist?list=PL6601A198DF14788D

[kay15] Alan Kay, 2015: [Power of Simplicity](https://www.youtube.com/watch?v=NdSD07U5uBs)

http://stephane.ducasse.free.fr/FreeBooks/

[blue] Adele Goldberg, David Robson
[Smalltalk-80: The Language and its Implementation](http://stephane.ducasse.free.fr/FreeBooks/BlueBook/Bluebook.pdf)
XeroxParc lab, Addison-Wesley, 1983

[little] Tim Budd [A Little Smalltalk](http://stephane.ducasse.free.fr/FreeBooks/LittleSmalltalk/ALittleSmalltalk.pdf) Addison-Wesley 1987

### Misc

[dbms] **Database Systems. The Complete Book** 2nd ed.
Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom

[hickey] https://www.youtube.com/watch?v=eWbPLSJZ5Zw

[mdmp] Vytautas à tuikys, Robertas Damaševičius
**Meta-Programming and Model-Driven Meta-Program Development: Principles,
Processes and Techniques**
Springer London, 2013, ISBN 978-1-4471-4126-6
