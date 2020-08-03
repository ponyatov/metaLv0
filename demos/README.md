#  `demos`
## `unikernel` OS model in metaL/py

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

github: https://github.com/ponyatov/metaL/blob/master/demos.py

It's an operating system model treated as a demo of writing a language-powered
OS in Python, which was mentioned in https://t.me/osdev channel a few weeks ago.
It is not something more than just a fun toy, not targets for any practical use
or Linux killer.

On the other side, I don't see a lot of projects on implementing hobby OS based
on some language interpreter, compiler embedded into the OS kernel, or
standalone interactive development system, as it was popular in the 80th.

So, in this demo, I'm going to mix a bytecode interpreter, a few bare-metal
drivers written in C and assembly, and the method of concept programming in
Python. Also, it should run in a *guest OS* mode as generic application over
mainstream OS such as Linux.

* hw: i386/QEMU
* powered by `metaL`
