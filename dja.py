## @file
## @brief Django Apps Generator

from metaL import *

## @defgroup dja Dja
## @ingroup py
## @brief Django Apps Generator
## @{

MODULE = pyModule('dja')

TITLE = Title('Generic Django App /metaL-templated/')
MODULE << TITLE

ABOUT = '''
Automatic (generative) programming approach to building intranet business systems:
* Python/Django/PostgreSQL stack
* powered by `metaL`
'''
MODULE['about'] = ABOUT

## `~/metaL/$MODULE` target directory for code generation
diroot = MODULE['dir']

## README
readme = README(MODULE)
diroot // readme
readme.sync()

## file masks will be ignored by `git` version manager
gitignore = diroot['gitignore']
gitignore.sync()

## Debian Linux packages install
apt = diroot['apt']

## `Makefile` for target project build/run
mk = diroot['mk']
# mk // (Section(MODULE) // '.PHONY: all\nall: $(PY) $(MODULE).py\n\t$^\n')
mk.sync()

## file associations in .vscode
MODULE['vscode/assoc'] // (' ' * 8 + '"**/templates/*.html": "html",')
MODULE['vscode/settings'].sync()

## requirements.txt
reqs = diroot['reqs']
reqs // 'django'
reqs.sync()

## main Python file
py = diroot['py']
py['head'] // MODULE.py()
py.sync()

## static files directory
static = Dir('static')
diroot // static
static.sync()
static // File('.gitignore')

## .html templates directory
templates = Dir('templates')
diroot // templates
templates.sync()
templates // File('.gitignore')

# print(MODULE)

## @}
