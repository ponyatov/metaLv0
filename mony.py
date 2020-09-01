## @file
## @brief Monitoring system

from metaL import *
from dja import *

## @defgroup mony mony
## @brief Monitoring system
## @ingroup dja
## @{

MODULE = djModule()

TITLE = Title('Monitoring System')
MODULE['TITLE'] = TITLE

ABOUT = """
Django-based (meta)project targets on building IT/sensor/IIoT monitoring system
for small business, SmartHome, etc.

* standalone (SQLite) & RDBMS
"""
MODULE['ABOUT'] = ABOUT

MODULE['GITHUB']['branch'] = '.py'

diroot = MODULE['dir']

readme = README(MODULE)
diroot // readme
readme.sync()

## @}
