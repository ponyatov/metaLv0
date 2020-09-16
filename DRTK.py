## @file
## @brief metaL model of dRTK: experimental distributed real-time operating system kernel
## book: K. Erciyes *Distributed Real-Time Systems: Theory and Practice*

from metaL import *
from drtos import *

## @defgroup drtk DRTK
## @ingroup os
## @brief `metaL` model of DRTK: experimental distributed real-time operating system kernel
##
## book: K. Erciyes *Distributed Real-Time Systems: Theory and Practice*
## [Springer'19](https://www.springer.com/gp/book/9783030225698)
## @{

MODULE = osModule()

TITLE = Title('DRTK: experimental distributed real-time operating system kernel')
MODULE['TITLE'] = TITLE

MODULE['ABOUT'] = ABOUT = '''
This `metaL` model implements the concept of the DRTK distributed realtime OS,
described in the book:
* Kayhan Erciyes *Distributed Real-Time Systems: Theory and Practice*

see this [book draft](https://www.notion.so/metalang/The-model-of-the-generic-OS-6ffc88fa84a2454cb63981e3656c7727) for more info.
'''

MODULE['README'] = README = README(MODULE)
diroot = MODULE['dir'] // README
README.sync()

## @}
