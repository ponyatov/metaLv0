## @file
## @brief Django Apps Generator

from metaL import *

## @defgroup dja Dja
## @ingroup py
## @brief Django Apps Generator
## @{

class djModule(pyModule):
    def __init__(self, V):
        pyModule.__init__(self,V)

MODULE = djModule('dja')

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
mk['head']['pytools'] // 'DJA = $(CWD)/bin/django-admin' // ''
mk['head'] // '' // 'HOST = 127.0.0.1'
mk['head'] // 'PORT = 19999' // ''
mk['all'] // '' // '.PHONY: runserver'
mk['all'] // 'runserver: $(PY) manage.py'
mk['all'] // '$^ runserver $(HOST):$(PORT)' // ''

mk['all'] // '.PHONY: migrations\nmigrations: $(PY) manage.py\n\t\t$^ make$@' // ''

mk['tail']['install'] // '\t$(MAKE) js'//''

js = Section('js/install') ; mk['tail'] // ''//js //''
js // '.PHONY: js'
js // 'js: static/jquery.js static/bootstrap.css static/bootstrap.js'
js // ''
js // 'JQUERY_VER = 3.5.0'
js // 'static/jquery.js:'
js // '\t$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js'
js // ''
js // 'BOOTSTRAP_VER = 3.4.1'
js // 'BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/'
js // 'static/bootstrap.css:'
js // '\t$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css'
js // 'static/bootstrap.js:'
js // '\t$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js'
js // ''
mk.sync()

## file associations in .vscode
MODULE['vscode/assoc'] // (' ' * 8 + '"**/templates/*.html": "html",')
MODULE['vscode/assoc'] // (' ' * 8 + '// "**/templates/*": "django-txt",')
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
