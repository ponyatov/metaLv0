## @file
## @brief metacircular implementation in metaL/py

## @defgroup circ Metacircular
## @brief `implementation in metaL/py`
## @{

from metaL import *

## `<module:metaL>` reimplements itself using host VM metainfo
MODULE = vm['MODULE']

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
