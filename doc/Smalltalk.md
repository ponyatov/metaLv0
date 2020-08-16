# Smalltalk {#stmd}

* **Free Online Smalltalk Books**
  http://stephane.ducasse.free.fr/FreeBooks.html
  * [Smalltalk-80: The Language and its Implementation](http://sdmeta.gforge.inria.fr/FreeBooks/BlueBook/)
    Adele Goldberg, DavidRobson; Xerox Palo Alto Research Center ISBN 0-201-11371-6. 344 pp. 1983

Smalltalk is a pure OOP programming language & interactive system, which uses
the message-passing paradigm even for very low-level computation such as math
operators and file I/O. This computation model is very interesting for
distributed and parallel computing, as messages can be passed between
computation nodes, and message late dispatch and async Actor model is very
friendly for networked distributed applications and load balancing between
isolated processes on the same computer.

Is it very sad, that Smalltalk was kicked off in 90th by C++ and Java due to its
comparable slow messaging vs direct machine code execution, and it also needs
more resources to be run. The original Xerox Research version was implemented on
a very costly Palo Alto computer with 1..2M of RAM. This amount of RAM was not
unavailable even on IBM PC-compatible personal computers until the i386
processor come.

With modern ugly JavaScript-powered systems Smalltalk drawbacks already do not
have any meanings. In reverse, its portability, flexibility, interactive
development, and development-in-debug have many more perspectives for business
systems (to be run over JVM mostly, or CPython runtime). The only problem is the
lack of interest from developers who never work with real handy Smalltalk
systems. This playlist can provide some overview:
* https://www.youtube.com/playlist?list=PL6601A198DF14788D

Another drawback is Smalltalk syntax. It is simple, but some aspect such as lack
of special syntax for data containers in the language core is not good. Maybe,
some language that mixes Pythonic syntax and Smalltalk async messaging can be
much much handy. So, here in `metaL` there is some Smalltalk model that was
created in experimenting with mixing Lispy functional programming with
message-passing computation. It is not required to be mixed in the same system,
as the `metaL` metaprogramming part can be fully separated from the target pure
Smalltalk implementation. Finally, CPython as the runtime is good because there
are a huge amount of libraries for any case, while it is very fast comparing to
JVM hell (memory and startup time is awful).
