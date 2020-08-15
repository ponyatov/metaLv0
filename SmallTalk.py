## @file
## @brief SmallTalk system model

from metaL import *

## @defgroup st SmallTalk
## @brief SmallTalk system model
## @{

MODULE = pyModule('SmallTalk')

TITLE = Title('SmallTalk system model')
MODULE << TITLE

ABOUT = '''
* powered by `metaL`
'''
MODULE['about'] = ABOUT

## `~/metaL/$MODULE` target directory for code generation
diroot = MODULE['dir']
## README
readme = README(MODULE)
diroot // readme
readme.sync()


print(MODULE)

## @}
