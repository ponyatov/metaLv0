## @file
## @brief Django Apps Generator

from metaL import *

## @defgroup dja Dja
## @ingroup py
## @brief Django Apps Generator
## @{

MODULE = Module('dja')
vm['MODULE'] = MODULE

TITLE = Title('Django Apps Generator')
vm['TITLE'] = TITLE

ABOUT = String('''
Automatic (generative) programming approach to building intranet business systems:
* Python/Django/PostgreSQL stack
* powered by `metaL`
''')
vm['ABOUT'] = ABOUT

## `~/metaL/$MODULE` target directory for code generation
diroot = Dir(MODULE)
vm['dir'] = diroot

## file masks will be ignored by `git` version manager
gitignore = pygIgnore('.gitignore')
vm['gitignore'] = gitignore
diroot // gitignore
gitignore.sync()

## `Makefile` for target project build/run
mk = pyMakefile()
vm['mk'] = mk
diroot // mk
mk // Section(MODULE)
mk.sync()

print(vm)

## @}
