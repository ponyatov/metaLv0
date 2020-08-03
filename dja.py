## @file
## @brief Django Apps Generator

from metaL import *

## @defgroup dja Dja
## @brief Django Apps Generator

vm['MODULE'] = MODULE = dja = Module('dja')
vm['TITLE'] = TITLE = Title('Django Apps Generator')

vm['dir'] = dirfile = Dir(MODULE)

vm['gitignore'] = gitignore = File('.gitignore')
dirfile // gitignore
gitignore // '*~\n*.swp'
gitignore // ''
gitignore // '*.log\n*.exe\n*.o'
gitignore // '''
*.pyc
/bin/
/include/
/lib/
/lib64/
/share/
pyvenv.cfg
config.py'''

print(vm)

## @}
