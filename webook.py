## @file
## @brief Web Book platform demo

## @defgroup webook webook
## @brief Web Book platform demo

## @{

from dja import *

MODULE = djModule('webook')

MODULE['URL'] = Url(
    'https://repl.it/talk/ask/Who-knows-any-micro-contest-platform-for-newbies-in-programming/49019')

MODULE['GITHUB'] = Url('https://repl.it/@metaLmasters/metaL#')

TITLE = Title('Web Book platform demo')
MODULE << TITLE

ABOUT = '''
%s

Demo web platform for newbies in programming runs over [Repl.it](https://repl.it) sandbox
* micro-contest rating subsystem
* programming cookbook making
* community blogging and modular tutorial writing
* Python/Django/PostgreSQL stack
* powered by `metaL`
''' % MODULE['URL'].val
MODULE['about'] = ABOUT


## `~/metaL/$MODULE` target directory for code generation
diroot = MODULE['dir']

## README
readme = README(MODULE)
diroot // readme
readme.sync()

print(MODULE)

## @}
