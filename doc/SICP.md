# SICP {#sicp}

* in Clojure
  * http://www.sicpdistilled.com
  * Wojtek Gawroński
    * http://www.afronski.pl/sicp-in-clojure/2015/06/04/sicp-in-clojure-chapter-1.html

### What is SICP and why it is important?

**SICP** is the classic Computer Science book **Structure and Interpretation of
Computer Programs** was written by Harold Abelson, Gerald Jay Sussman, and Julie
Sussman. Original was written in Scheme is a very popular Lisp dialect. Nowadays
having Java stack crawled off everywhere, it is much better to use the JVM-based
Lisp dialect called Clojure. It has some differences from the classical Lisp,
mostly in data/program representation and syntax, which is more comfortable for
software transformation tasks.

This book is important here, as it is the most known book on using and
implementing reflective programming language system. So, the `metaL` uses some
elements from this book, sugared by script syntax, and Python-based runtime.
Another potential directing is porting `metaL` core to Clojure, to run it under
enterprise-grade infrastructure, interact with Java-specific services and
frameworks such as Kafka, Spark, and Spring, including writing software for Java
& Android world.