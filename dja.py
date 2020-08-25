## @file
## @brief Django Apps Generator

from metaL import *

## @defgroup dja Dja
## @ingroup py
## @brief Django Apps Generator
## @{

## Django-related models
class DJ(Object):
    pass

## route controller (url+view+template?)
class djRoute(DJ):

    ## codegen for `views.py`
    def py_view(self):
        s = "\ndef %s(request): # %s" % (self.val, self.head(test=True))
        s += "\n\ttemplate = loader.get_template('%s.html')" % self.val
        s += "\n\tcontext = {}"
        s += "\n\treturn HttpResponse(template.render(context, request))"
        return s

    ## codegen for `urls.py`
    ## @param[in] route path in browser
    ## @param[in] request processing function
    def py_url(self, route=None, request=None):
        if route == None:
            route = '%s/' % self.val
        if request == None:
            request = 'views.%s' % self.val
        return "\tpath('%s', %s, name='%s')," % (route, request, self.val)

class djModule(DJ, pyModule):
    def __init__(self, V=None):
        pyModule.__init__(self, V)
        # requirements.txt
        self.reqs.metal.dropall()
        self.reqs // 'django'
        self.reqs.sync()
        # .gitignore
        self.gitignore.bot // ('/%sz/' % self.val)
        # routes
        self.index = djRoute('index')
        self.admin = djRoute('admin')
        # app
        self.init_app()
        # manage.py
        self.init_manage()
        # static
        self.init_static()
        # templates
        self.init_templates()
        # tasks
        self.init_tasks()
        # templates
        self.init_templates()

    def init_tasks(self):
        pyModule.init_tasks(self)
        self.tasks.mid // '\t\t{'
        self.tasks.mid // '\t\t\t"label": "Django: migrate",'
        self.tasks.mid // '\t\t\t"type": "shell",'
        self.tasks.mid // '\t\t\t"command": "make migrate",'
        self.tasks.mid // '\t\t\t"problemMatcher": []'
        self.tasks.mid // '\t\t},'
        self.tasks.mid // '\t\t{'
        self.tasks.mid // '\t\t\t"label": "Django: makemigrations",'
        self.tasks.mid // '\t\t\t"type": "shell",'
        self.tasks.mid // '\t\t\t"command": "make makemigrations",'
        self.tasks.mid // '\t\t\t"problemMatcher": []'
        self.tasks.mid // '\t\t},'
        self.tasks.sync()

    def init_static(self):
        self['static'] = self.static = Dir('static')
        self.diroot // self.static
        self.static.sync()
        self.static // File('.gitignore')

    def init_templates(self):
        self['templates'] = self.templates = Dir('templates')
        self.diroot // self.templates
        self.templates.sync()
        self.templates // File('.gitignore')
        self.init_templates_all()
        self.init_templates_index()

    def init_templates_all(self):
        self.templates['all'] = self.templates.all = File(
            'all.html', comment=None)
        self.templates // self.templates.all
        self.templates.all // '<!DOCTYPE html>'
        self.templates.all // '<html lang="ru">'
        self.templates.all // '\t<head>' //\
            '\t\t<meta charset="utf-8">' //\
            '\t\t<meta http-equiv="X-UA-Compatible" content="IE=edge">' //\
            '\t\t<meta name="viewport" content="width=device-width, initial-scale=1">' //\
            '\t\t{% block title %}{% endblock %}' //\
            '\t\t<link href="/static/bootstrap.css" rel="stylesheet">' //\
            '\t</head>'
        self.templates.all // '\t<body>' //\
            '\t\t{% block body %}{% endblock %}' //\
            '\t\t<script src="/static/jquery.js"></script>' //\
            '\t\t<script src="/static/bootstrap.js"></script>' //\
            '\t</body>'
        self.templates.all // '</html>'
        self.templates.all.sync()

    def init_templates_index(self):
        self.templates['index'] = self.templates.index = File(
            'index.html', comment=None)
        self.templates // self.templates.index
        self.templates.index // "{% extends 'all.html' %}" // ''
        self.templates.index.sync()

    def init_app(self):
        self.app = self['app'] = Dir('app')
        self.diroot // self.app
        self.app // pyFile('__init__')
        self.mk.src.drop() # config.py
        self.mk.src.drop() # $(module).py
        self.init_app_settings()
        self.init_app_views()
        self.init_app_urls()

    def init_app_i18n(self):
        self.app['i18n'] = self.app.i18n = Section('i18n')
        self.app.settings.mid // self.app.i18n
        self.app.i18n // "LANGUAGE_CODE = 'ru-ru'"#'en-us'"
        # self.app.i18n // "USE_I18N = True"
        # self.app.i18n // "USE_L10N = True"
        # self.app.i18n // "TIME_ZONE = 'UTC'"
        # self.app.i18n // "USE_TZ = True"

    def init_app_settings(self):
        self.app['settings'] = self.app.settings = pyFile('settings')
        self.app // self.app.settings
        self.app.settings.top // '## @brief Django settings'
        self.app.settings.top // 'from pathlib import Path'
        self.app.settings.mid // 'BASE_DIR = Path(__file__).resolve(strict=True).parent.parent'
        self.app.settings.top // pyImport('os')
        self.app.settings.mid // 'SECRET_KEY = os.urandom(64)'
        self.app.settings.mid // 'DEBUG = True'
        self.app.settings.mid // 'ALLOWED_HOSTS = []'
        self.init_app_installed()
        self.init_app_static()
        self.app_init_middleware()
        self.app.settings.mid // "ROOT_URLCONF = 'app.urls'"
        self.init_app_templates()
        self.init_app_databases()
        self.init_app_i18n()
        self.app.settings.sync()
        self.mk.src // 'SRC += app/settings.py'
        self.mk.sync()

    def app_init_middleware(self):
        self.app.settings.mid // 'MIDDLEWARE = ['
        self.app['middleware'] = self.app.middleware = Section('middleware')
        self.app.settings.mid // self.app.middleware
        self.app.settings.mid // ']'
        # self.app.middleware // "\t'django.middleware.security.SecurityMiddleware',"
        self.app.middleware // "\t'django.contrib.sessions.middleware.SessionMiddleware',"
        self.app.middleware // "\t'django.contrib.auth.middleware.AuthenticationMiddleware',"
        self.app.middleware // "\t'django.contrib.messages.middleware.MessageMiddleware',"

    def init_app_templates(self):
        self.app.settings.mid // 'TEMPLATES = ['
        self.app['templates'] = self.app.templates = Section('templates')
        self.app.settings.mid // self.app.templates
        self.app.settings.mid // ']'
        self.app.templates // '\t{'
        self.app.templates // "\t\t'BACKEND': 'django.template.backends.django.DjangoTemplates',"
        # self.app.templates // "\t\t'DIRS': [],"
        # req for /template resolve
        self.app.templates // "\t\t'DIRS': [BASE_DIR/'templates'],"
        self.app.templates // "\t\t'APP_DIRS': True," # req for admin/login.html template
        self.app.templates // "\t\t'OPTIONS': {"
        self.app.templates // "\t\t\t'context_processors': ["
        # self.app.templates // "\t\t\t'django.template.context_processors.debug',"
        self.app.templates // "\t\t\t\t'django.template.context_processors.request',"
        self.app.templates // "\t\t\t\t'django.contrib.auth.context_processors.auth',"
        self.app.templates // "\t\t\t\t'django.contrib.messages.context_processors.messages',"
        self.app.templates // '\t\t\t],'
        self.app.templates // '\t\t},'
        self.app.templates // '\t},'

    def init_app_databases(self):
        self.app.settings.mid // "DATABASES = {"
        self.app['databases'] = self.app.databases = Section('databases')
        self.app.settings.mid // self.app.databases
        self.app.databases // "\t'default': {"
        self.app.databases // "\t\t'ENGINE': 'django.db.backends.sqlite3',"
        self.app.databases // ("\t\t'NAME': BASE_DIR / '%s.sqlite3'," % self.val)
        self.app.databases // "\t}"
        self.app.settings.mid // "}"

    def init_app_installed(self):
        self.app['installed'] = self.app.installed = Section('installed')
        self.app.settings.mid // 'INSTALLED_APPS = [' // self.app.installed // ']'
        self.app.installed // "\t'django.contrib.admin',"
        self.app.installed // "\t'django.contrib.auth',"
        self.app.installed // "\t'django.contrib.contenttypes',"
        self.app.installed // "\t'django.contrib.sessions',"
        self.app.installed // "\t'django.contrib.messages',"

    def init_app_static(self):
        self.app.installed // "\t'django.contrib.staticfiles',"
        self.app.settings.bot // "STATIC_URL = '/static/'"

    def init_app_views(self):
        self.app['views'] = self.app.views = pyFile('views')
        self.app // self.app.views
        self.app.views.top // "from django.http import HttpResponse"
        self.app.views.top // "from django.template import loader"
        self.app.views.mid // self.index.py_view()
        self.app.views.sync()

    def init_app_urls(self):
        self.app['urls'] = self.app.urls = pyFile('urls')
        self.app // self.app.urls
        self.app.urls.top // '## @brief URL routing'
        self.app.urls.top // 'from django.contrib import admin'
        self.app.urls.top // 'from django.urls import path' // ''
        self.app.urls.top // 'from . import views' // ''
        self.app.urls.top // 'urlpatterns = ['
        self.app.urls.mid // self.index.py_url(route='')
        self.app.urls.mid // self.admin.py_url(request='admin.site.urls')
        self.app.urls.bot // ']'
        self.app.urls.sync()
        self.mk.src // 'SRC += app/urls.py'
        self.mk.sync()

    def init_py(self):
        pyModule.init_py(self)
        os.remove('%s/%s.py' % (self.diroot.val, self.diroot.val))
        os.remove('%s/metaL.py' % self.diroot.val)
        os.remove('%s/config.py' % self.diroot.val)
        self.py.metal.dropall()
        self.py.bot.dropall()
        self.py.sync()

    ## `.gitignore` callback from `anyModule.__init__()``
    def init_gitignore(self):
        pyModule.init_gitignore(self)
        self.gitignore.mid // ("%s.sqlite3" % self.val)
        self.gitignore.bot // ('/%sz/' % self.val)
        self.gitignore.sync()

    def init_manage(self):
        self.manage = self['manage'] = pyFile('manage')
        self.mksrc(self.manage)
        self.diroot // self.manage
        self.manage.top // ('## @file %s' % self.file())
        self.manage.top // pyImport('os') // pyImport('sys')
        self.manage.main = pyFn('main')
        self.manage.main // (
            "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')")
        self.manage.main // "from django.core.management import execute_from_command_line"
        self.manage.main // "execute_from_command_line(sys.argv)"
        self.manage.mid // self.manage.main
        self.manage.bot // "if __name__ == '__main__':"
        self.manage.bot // '\tmain()'
        self.manage.sync()

    def init_mk(self):
        pyModule.init_mk(self)
        # Makefile
        self.mk['all']['repl'].dropall()
        self.mk.src // 'SRC += manage.py'
        self.mk.all // '.PHONY: all\nall: $(PY) manage.py\n\t$^'
        # install
        self.mk.install // '\t$(MAKE) migrate'
        self.mk.install // '\t$(MAKE) createsuperuser'
        # runserver
        runserver = Section('runserver')
        runserver // '.PHONY: runserver\nrunserver: $(PY) manage.py\n\t$^ $@'
        self.mk.mid // runserver
        # check
        self.mk.mid // (Section('check') //
                        '.PHONY: check\ncheck: $(PY) manage.py\n\t$^ $@')
        # makemigrations
        makemigrations = Section('makemigrations')
        self.mk.mid // makemigrations
        makemigrations // '.PHONY: makemigrations\nmakemigrations: $(PY) manage.py\n\t$^ $@'
        # migrate
        migrate = Section('migrate')
        self.mk.mid // migrate
        migrate // '.PHONY: migrate\nmigrate: $(PY) manage.py\n\t$^ $@'
        # createsuperuser
        createsuperuser = Section('createsuperuser')
        self.mk.mid // createsuperuser
        createsuperuser // '.PHONY: createsuperuser\ncreatesuperuser: $(PY) manage.py\n\t$^ $@'
        # shell
        shell = Section('shell')
        shell // '.PHONY: shell\nshell: $(PY) manage.py\n\t$^ $@'
        self.mk.mid // shell
        # manage
        startproject = Section('startproject')
        self.mk.mid // startproject
        startproject // '.PHONY: startproject'
        startproject // 'startproject: bin/django-admin'
        startproject // ('\t$< startproject %sz' % self.val)
        self.mk.sync()

    def init_settings(self):
        pyModule.init_settings(self)
        self.settings.f11 // 'make runserver'
        self.settings.f12 // 'make check'
        self.settings.sync()


# MODULE = djModule('dja')

# TITLE = Title('Generic Django App /metaL-templated/')
# MODULE << TITLE

# ABOUT = '''
# Automatic (generative) programming approach to building intranet business systems:
# * Python/Django/PostgreSQL stack
# * powered by `metaL`
# '''
# MODULE['about'] = ABOUT

# ## `~/metaL/$MODULE` target directory for code generation
# diroot = MODULE['dir']

# ## README
# readme = README(MODULE)
# diroot // readme
# readme.sync()

# ## file masks will be ignored by `git` version manager
# gitignore = diroot['gitignore']
# gitignore.sync()

# ## Debian Linux packages install
# apt = diroot['apt']

# ## `Makefile` for target project build/run
# mk = diroot['mk']
# mk['head']['pytools'] // 'DJA = $(CWD)/bin/django-admin' // ''
# mk['head'] // '' // 'HOST = 127.0.0.1'
# mk['head'] // 'PORT = 19999' // ''
# mk['all'] // '' // '.PHONY: runserver'
# mk['all'] // 'runserver: $(PY) manage.py'
# mk['all'] // '$^ runserver $(HOST):$(PORT)' // ''

# mk['all'] // '.PHONY: migrations\nmigrations: $(PY) manage.py\n\t\t$^ make$@' // ''

# mk['tail']['install'] // '\t$(MAKE) js'//''

# js = Section('js/install') ; mk['tail'] // ''//js //''
# js // '.PHONY: js'
# js // 'js: static/jquery.js static/bootstrap.css static/bootstrap.js'
# js // ''
# js // 'JQUERY_VER = 3.5.0'
# js // 'static/jquery.js:'
# js // '\t$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js'
# js // ''
# js // 'BOOTSTRAP_VER = 3.4.1'
# js // 'BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/'
# js // 'static/bootstrap.css:'
# js // '\t$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css'
# js // 'static/bootstrap.js:'
# js // '\t$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js'
# js // ''
# mk.sync()

# ## file associations in .vscode
# MODULE['vscode/assoc'] // (' ' * 8 + '"**/templates/*.html": "html",')
# MODULE['vscode/assoc'] // (' ' * 8 + '// "**/templates/*": "django-txt",')
# MODULE['vscode/settings'].sync()

# ## requirements.txt
# reqs = diroot['reqs']
# reqs // 'django'2
# reqs.sync()

# ## main Python file
# py = diroot['py']
# py['head'] // MODULE.py()
# py.sync()

# ## static files directory
# static = Dir('static')
# diroot // static
# static.sync()
# static // File('.gitignore')

# ## .html templates directory
# templates = Dir('templates')
# diroot // templates
# templates.sync()
# templates // File('.gitignore')

# # print(MODULE)

## @}
