## @file
## @brief `unikernel` OS model

from metaL import *

## @defgroup demos demos
## @ingroup gen
## @brief `unikernel` OS model
## @{

MODULE = Module('demos')
vm['MODULE'] = MODULE

TITLE = Title('`unikernel` OS model')
vm['TITLE'] = TITLE

ABOUT = String('''
* hw: i386/QEMU
* powered by `metaL`
''')
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


print(vm)

## @}
