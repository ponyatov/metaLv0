#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file <vm:metaL>
# \ <section:metaL>
from metaL import *

MODULE = pyModule('webook')

TITLE = Title('')
MODULE << TITLE

## `~/metaL/$MODULE` target directory for code generation
diroot = MODULE['dir']

## README
readme = README(MODULE)
diroot // readme
readme.sync()

## module source code
py = diroot['py']
py['head'] // ('## @brief %s' % MODULE['title'].val) // ''
py.sync()
# / <section:metaL>
