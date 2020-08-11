## @file
## @brief SQLite-based generic RDBMS model (not API client/interfacing library)

## @defgroup rdbms rdbms
## @brief SQLite-based generic RDBMS model (not API client/interfacing library)
## @{

from metaL import *

MODULE = pyModule('rdbms')

TITLE = Title('SQLite-based generic RDBMS model')
MODULE << TITLE

ABOUT = '''
This module targets on a generalization of RDBMS engine design in the form of
`metaL` model. Templating of DBMS elements and algorithms. It is not an API
client/interfacing library, see `metaL/sqlite.py` for ORM implementation.
'''
MODULE['about'] = ABOUT

diroot = MODULE['dir']

## README
readme = README(MODULE)
diroot // readme
readme // '''
### Links

* https://github.com/sqlite/sqlite

[dbms] **Database Systems. The Complete Book** 2nd ed.
Hector Garcia-Molina, Jeffrey D. Ullman, Jennifer Widom'''
readme.sync()

## main Python file
py = diroot['py']
py['head'] // MODULE.py()
py.sync()

MODULE

## @}
