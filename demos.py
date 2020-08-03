## @file
## @brief `unikernel` OS model

from metaL import *

## @defgroup demos demos
## @brief `unikernel` OS model
## @{

MODULE = Module('demos')
vm['MODULE'] = MODULE

TITLE = Title('`unikernel` OS model in metaL/py')
vm['TITLE'] = TITLE

ABOUT = String('''
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
* powered by `metaL`''')
vm['ABOUT'] = ABOUT

## `~/metaL/$MODULE` target directory for code generation
diroot = Dir(MODULE)
vm['dir'] = diroot

## file masks will be ignored by `git` version manager
gitignore = gitIgnore('.gitignore')
vm['gitignore'] = gitignore
diroot // gitignore
gitignore.sync()

## `Makefile` for target project build/run
mk = Makefile()
vm['mk'] = mk
diroot // mk
mk // Section(MODULE)
mk.sync()

## `README.md`
readme = File('README.md')
diroot // readme
readme // ('#  `%s`' % MODULE.val)
readme // ('## %s' % TITLE.val)
readme // ''
readme // ('(c) %s <<%s>> %s %s' %
           (AUTHOR.val, EMAIL.val, YEAR.val, LICENSE.val))
readme // ''
readme // ('github: %s/%s/blob/master/%s.py' %
           (GITHUB.val, vm.val, MODULE.val))
readme // ABOUT
readme.sync()


print(vm)

## @}
