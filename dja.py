## @file
## @brief Django Apps Generator

from metaL import *

## @defgroup dja Dja
## @brief Django Apps Generator
## @{

## Django-related models
## @ingroup dja
class DJ(Object):
    pass

## route controller (url+view+template?)
## @ingroup dja
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

## plugin
## @ingroup dja
class djPlugin(DJ, Module):
    pass


## @ingroup dja
## `GeoDjango` GIS subsystem
## * https://krzysztofzuraw.com/blog/2016/geodjango-leaflet-part-one.html
## * https://krzysztofzuraw.com/blog/2016/geodjango-leaflet-part-two.html
geodjango = djPlugin('geodjango')

## Django minimal project
## @ingroup dja
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
        # proj
        self.init_proj()
        # app
        self.init_app()
        # manage.py
        self.init_manage()
        # setup.py
        self.init_install()
        # static
        self.init_static()
        # templates
        self.init_templates()
        # tasks
        self.init_tasks()
        # templates
        self.init_templates()
        # admin
        self.init_admin()
        # models
        self.init_models()
        # cotext processors
        self.init_contexts()
        # migrations
        self.init_migrations()

    def init_migrations(self):
        self['migrations'] = self.migrations = Dir('migrations')
        self.app // self.migrations
        self.migrations.sync()
        self.migrations // File('__init__.py').sync()
        giti = File('.gitignore', comment=None)
        self.migrations // giti
        giti // '????_*.py'
        giti.sync()
        # self.migrations.user = pyFile('0000_initial')
        # self.migrations // self.migrations.user
        # self.migrations.user.top // "from django.conf import settings"
        # self.migrations.user.top // "from django.db import migrations, models"
        # self.migrations.user.mid // "class Migration(migrations.Migration):"
        # self.migrations.user.mid // "\tdependencies = ["
        # self.migrations.user.mid // "\t\tmigrations.swappable_dependency(settings.AUTH_USER_MODEL),"
        # self.migrations.user.mid // "\t]"
        # self.migrations.user.mid // "\toperations = ["
        # self.migrations.user.mid // "\t]"
        # self.migrations.user.sync()

    def init_install(self):
        self.diroot['install'] = self.proj.install = pyFile('install')
        self.diroot // self.proj.install
        self.proj.install.top //\
            'import os' //\
            'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")' //\
            'import django' //\
            'django.setup()' //\
            'from django.contrib.auth.models import User'
        self.proj.install.mid //\
            'su = User.objects.create_superuser(' //\
            "\tusername='dponyatov'," //\
            "\temail='dponyatov@gmail.com'," //\
            "\tpassword='passwd'" //\
            ')' //\
            'su.save()'
        self.proj.install.sync()
        self.mk.install // '\t$(MAKE) createsuperuser'
        # self.mk.install // '\t$(PY) install.py'
        self.mk.sync()

    def init_contexts(self):
        self.proj['context'] = self.proj.context = pyFile('context')
        self.proj // self.proj.context
        self.proj.context.top // 'from django.contrib.auth.models import User'
        # self.proj.context.mid // "\tuser = request.user"
        # self.proj.context.mid // "\tuser.f = 'Фамилия'"
        # self.proj.context.mid // "\tuser.i = 'Имя'"
        # self.proj.context.mid // "\tuser.o = 'Отчество'"
        # self.proj.context.mid // "\tuser.email = 'no@mail.ru'"
        # self.proj.context.mid // "\tuser.tel = '+79171234567'"
        self.proj.context.mid //\
            "from app.apps import AppConfig" //\
            "def title(request):" //\
            "\treturn {'title':AppConfig.verbose_name}" //\
            ''
        self.proj.context.mid //\
            'def user(request):' //\
            '\ttry:' //\
            "\t\tuser = User.objects.get(id=request.user.id)" //\
            "\texcept User.DoesNotExist:" //\
            "\t\tuser = None" //\
            "\treturn {'user':user}" //\
            self.proj.context.sync()

    def init_admin(self):
        self.app['admin'] = self.proj.admin = pyFile('admin')
        self.app // self.proj.admin
        self.proj.admin.top // 'from django.contrib import admin'
        self.proj.admin.mid // 'from .models import *'
        self.proj.admin.sync()

    def init_models(self):
        self['models'] = self.models = pyFile('models')
        self.app // self.models
        self.models.top // '# https://tproger.ru/translations/extending-django-user-model/#var2'
        self.models.top // "from django.db import models"
        #
        user = Section('user')
        self.models.mid // user
        user //\
            "from django.contrib.auth.models import AbstractUser" //\
            "class CustomUser(AbstractUser):" //\
            "\tpass"
        user.sync()
        #
        location = Section('location')
        self.models.mid // location
        self.proj.admin.bot // 'admin.site.register(Location)'
        location // 'class Location(models.Model):' //\
            "\tname = models.CharField('название', max_length=0x22, blank=False)" //\
            "\tclass Meta:" //\
            "\t\tverbose_name = 'регион'" //\
            "\t\tverbose_name_plural = 'регионы'" //\
            "\tdef __str__(self):" //\
            "\t\treturn '%s'%self.name"
        # profile = Section('profile')
        # self.models.mid // profile
        # self.proj.admin.bot // 'admin.site.register(Profile)'
        # profile // "class Profile(models.Model):" //\
        # "from django.contrib.auth.models import User"//\
        #     "\tuser = models.OneToOneField(User, verbose_name='пользователь', on_delete=models.CASCADE)" //\
        #     "\tloc = models.ForeignKey(Location, verbose_name='регион', on_delete=models.DO_NOTHING)" //\
        #     "\tphone = models.CharField('телефон',max_length=0x11,blank=True)" //\
        #     "\tclass Meta:" //\
        #     "\t\tverbose_name = 'профиль пользователя'" //\
        #     "\t\tverbose_name_plural = 'профили пользователей'" //\
        #     "\tdef __str__(self):" //\
        #     "\t\treturn '%s @ %s | %s'%(self.user,self.loc,self.phone)"
        self.models.sync()
        self.proj.admin.sync()
        self.mk.src // 'SRC += app/models.py'
        self.mk.sync()

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
        giti = File('.gitignore', comment=None)
        self.static // giti
        (giti // 'bootstrap.*' // 'jquery.js').sync()

    def init_templates(self):
        self['templates'] = self.templates = Dir('templates')
        self.diroot // self.templates
        self.templates.sync()
        self.templates // File('.gitignore')
        self.init_templates_all()
        self.init_templates_index()
        admin = Dir('admin')
        self.templates // admin
        admin.sync()
        self.mk.src // 'SRC += app/admin.py'
        self.mk.sync()
        base_site = File('base_site.html', comment=None)
        admin // base_site
        base_site //\
            '{% extends "admin/base_site.html" %}' //\
            '{% load static %}' //\
            '{% block extrahead %}' //\
            '<link rel="shortcut icon" href="{% static "logo.png" %}" type="image/png">' //\
            '<style>' //\
            '* { background:#111 !important; color: #aaa; }' //\
            'input,select { background-color: lightyellow !important; color:black !important; }' //\
            'a:hover { color:lightblue; }' //\
            '.required { color:yellow !important; }' //\
            '</style>' //\
            '{% endblock %}'
        base_site.sync()

    def init_templates_all(self):
        self.templates['all'] = self.templates.all = File(
            'all.html', comment=None)
        self.templates // self.templates.all
        self.templates.all // '{% load static %}'
        self.templates.all // '<!DOCTYPE html>'
        self.templates.all // '<html lang="ru">'
        self.templates.all // '\t<head>' //\
            '\t\t<meta charset="utf-8">' //\
            '\t\t<meta http-equiv="X-UA-Compatible" content="IE=edge">' //\
            '\t\t<meta name="viewport" content="width=device-width, initial-scale=1">' //\
            '\t\t{% block title %}<title>{{title}}</title>{% endblock %}' //\
            '\t\t<link href="{% static "bootstrap.css" %}" rel="stylesheet">' //\
            '\t\t<link rel="shortcut icon" href="{% static "logo.png" %}" type="image/png">' //\
            '\t</head>'
        self.templates.all //\
            "\t<style>" //\
            "\t\tbody { padding:4mm; }" //\
            "\t\t@media print {" //\
            "\t\t\tbody { padding:0; }" //\
            "\t\t\ta[href]:after { display: none !important; }" //\
            "\t\t}" //\
            "\t</style>"
        self.templates.all // '\t<body>' //\
            '\t\t{% block body %}{% endblock %}' //\
            '\t\t<script src="{% static "jquery.js" %}"></script>' //\
            '\t\t<script src="{% static "bootstrap.js" %}"></script>' //\
            '\t</body>'
        self.templates.all // '</html>'
        self.templates.all.sync()

    def init_templates_index(self):
        self.templates['index'] = self.templates.index = File(
            'index.html', comment=None)
        self.templates // self.templates.index
        self.templates.index.top // "{% extends 'all.html' %}"
        self.templates.index.top // "{% load static %}" // ''
        self.templates.index.sync()

    def init_proj(self):
        self.proj = self['proj'] = Dir('proj')
        self.diroot // self.proj
        self.proj.sync()
        self.proj // pyFile('__init__')

    ## `/app/apps.py`
    def init_app(self):
        self.app = self['app'] = Dir('app')
        self.diroot // self.app
        self.app.sync()
        self.app // pyFile('__init__')
        self.mk.src.drop() # config.py
        self.mk.src.drop() # $(module).py
        self.init_app_settings()
        self.init_proj_views()
        self.init_proj_urls()
        self.app['apps'] = self.app.apps = pyFile('apps')
        self.app // self.app.apps
        self.app.apps.top // 'from django.apps import AppConfig'
        self.app.apps.mid // "class AppConfig(AppConfig):"
        self.app.apps.mid // "\tname = 'app'"
        self.app.apps.mid // ("\tverbose_name = '%s'" % self['TITLE'].val)
        self.app.apps.sync()
        self.mk.src // 'SRC += app/apps.py'
        self.mk.src.sync()

    ## intercept `A[key]=B` operations
    def __setitem__(self, key, that):
        super().__setitem__(key, that)
        if isinstance(that, Title):
            self.init_app()

    def init_proj_i18n(self):
        self.app['i18n'] = self.proj.i18n = Section('i18n')
        self.proj.settings.mid // self.proj.i18n
        self.proj.i18n // "LANGUAGE_CODE = 'ru-ru'"#'en-us'"
        # self.proj.i18n // "USE_I18N = True"
        # self.proj.i18n // "USE_L10N = True"
        # self.proj.i18n // "TIME_ZONE = 'UTC'"
        # self.proj.i18n // "USE_TZ = True"

    def init_app_settings(self):
        self.proj['settings'] = self.proj.settings = pyFile('settings')
        self.proj // self.proj.settings
        self.proj.settings.top // '## @brief Django settings'
        self.proj.settings.top // 'from pathlib import Path'
        self.proj.settings.mid // 'BASE_DIR = Path(__file__).resolve(strict=True).parent.parent'
        self.proj.settings.top // pyImport('os')
        self.proj.settings.mid // 'SECRET_KEY = "abcdefgh"#"os.urandom(64)"'
        self.proj.settings.mid // 'DEBUG = True'
        self.proj.settings.mid // 'ALLOWED_HOSTS = []'
        self.init_proj_installed()
        self.proj.settings.mid // "AUTH_USER_MODEL = 'app.CustomUser'"
        self.app_init_middleware()
        self.proj.settings.mid // "ROOT_URLCONF = 'proj.urls'"
        self.init_proj_templates()
        self.init_proj_databases()
        self.init_proj_i18n()
        self.init_proj_static()
        self.proj.settings.sync()
        self.mk.src // 'SRC += app/settings.py'
        self.mk.sync()

    def app_init_middleware(self):
        self.proj.settings.mid // 'MIDDLEWARE = ['
        self.app['middleware'] = self.proj.middleware = Section('middleware')
        self.proj.settings.mid // self.proj.middleware
        self.proj.settings.mid // ']'
        # self.proj.middleware // "\t'django.middleware.security.SecurityMiddleware',"
        self.proj.middleware // "\t'django.contrib.sessions.middleware.SessionMiddleware',"
        self.proj.middleware // "\t'django.contrib.auth.middleware.AuthenticationMiddleware',"
        self.proj.middleware // "\t'django.contrib.messages.middleware.MessageMiddleware',"

    def init_proj_templates(self):
        self.proj.settings.mid // 'TEMPLATES = ['
        self.app['templates'] = self.proj.templates = Section('templates')
        self.proj.settings.mid // self.proj.templates
        self.proj.settings.mid // ']'
        self.proj.templates // '\t{'
        self.proj.templates // "\t\t'BACKEND': 'django.template.backends.django.DjangoTemplates',"
        # self.proj.templates // "\t\t'DIRS': [],"
        # req for /template resolve
        self.proj.templates // "\t\t'DIRS': [BASE_DIR/'templates'],"
        # req for admin/login.html template
        self.proj.templates // "\t\t'APP_DIRS': True,"
        self.proj.templates // "\t\t'OPTIONS': {"
        self.proj.templates // "\t\t\t'context_processors': ["
        # self.proj.templates // "\t\t\t'django.template.context_processors.debug',"
        self.proj.templates // "\t\t\t\t'django.template.context_processors.request',"
        self.proj.templates // "\t\t\t\t'django.contrib.auth.context_processors.auth',"
        self.proj.templates // "\t\t\t\t'django.contrib.messages.context_processors.messages',"
        self.proj.templates // "\t\t\t\t'proj.context.user', 'proj.context.title', "
        self.proj.templates // '\t\t\t],'
        self.proj.templates // '\t\t},'
        self.proj.templates // '\t},'

    def init_proj_databases(self):
        self.proj.settings.mid // "DATABASES = {"
        self.proj['databases'] = self.proj.databases = Section('databases')
        self.proj.settings.mid // self.proj.databases
        self.proj.databases // "\t'default': {"
        self.proj.databases // "\t\t'ENGINE': 'django.db.backends.sqlite3',"
        self.proj.databases // ("\t\t'NAME': BASE_DIR/'%s.sqlite3'," % self.val)
        self.proj.databases // "\t}"
        self.proj.settings.mid // "}"

    def init_proj_installed(self):
        self.app['installed'] = self.proj.installed = Section('installed')
        self.proj.settings.mid // 'INSTALLED_APPS = [' // self.proj.installed // ']'
        self.proj.installed //\
            "\t'django.contrib.admin'," //\
            "\t'django.contrib.auth'," //\
            "\t'django.contrib.contenttypes'," //\
            "\t'django.contrib.sessions'," //\
            "\t'django.contrib.messages'," //\
            "\t'django.contrib.staticfiles'," //\
            "\t'app',"

    def init_proj_static(self):
        static = Section('static')
        self.proj.settings.mid // static
        static // "STATIC_URL = '/static/'"
        static // "STATICFILES_DIRS = [BASE_DIR/'static']"

    def init_proj_views(self):
        self.app['views'] = self.proj.views = pyFile('views')
        self.app // self.proj.views
        self.proj.views.top // "from django.http import HttpResponse"
        self.proj.views.top // "from django.template import loader"
        self.proj.views.mid // self.index.py_view()
        self.proj.views.sync()

    def init_proj_urls(self):
        self.proj['urls'] = self.proj.urls = pyFile('urls')
        self.proj // self.proj.urls
        self.proj.urls.top // '## @brief URL routing'
        self.proj.urls.top // 'from django.contrib import admin'
        self.proj.urls.top // 'from django.urls import path' // ''
        self.proj.urls.top // 'from app import views' // ''
        self.proj.urls.top // 'urlpatterns = ['
        self.proj.urls.mid // self.index.py_url(route='')
        self.proj.urls.mid // self.admin.py_url(request='admin.site.urls')
        self.proj.urls.bot // ']'
        self.proj.urls.sync()
        self.mk.src // 'SRC += proj/urls.py'
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
            "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')")
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
        self.mk.install // '\t$(MAKE) js'
        self.mk.install // '\t$(MAKE) migrate'
        js = Section('js/install')
        self.mk.bot // js
        js // ".PHONY: js"
        js // "js: static/jquery.js static/bootstrap.css static/bootstrap.js"
        js // ''
        js // "JQUERY_VER = 3.5.0"
        js // "static/jquery.js:"
        js // "\t$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js"
        js // ''
        js // "BOOTSTRAP_VER = 3.4.1"
        js // "BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/"
        js // "static/bootstrap.css:"
        js // "\t$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css"
        js // "static/bootstrap.js:"
        js // "\t$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js"
        js.sync()
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
        makemigrations // '.PHONY: makemigrations\nmakemigrations: $(PY) manage.py\n\t$^ $@ app'
        # migrate
        migrate = Section('migrate')
        self.mk.mid // migrate
        migrate // '.PHONY: migrate\nmigrate: $(PY) manage.py'
        migrate // '\t$(MAKE) makemigrations'
        migrate // '\t$^ $@'
        # createsuperuser
        createsuperuser = Section('createsuperuser')
        self.mk.mid // createsuperuser
        createsuperuser // '.PHONY: createsuperuser\ncreatesuperuser: $(PY) manage.py'
        createsuperuser // '\t$^ $@ \\'
        createsuperuser // ('\t\t--username %s \\' %
                            self['EMAIL'].val.split('@')[0])
        createsuperuser // ('\t\t--email %s' % self['EMAIL'].val)
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

## @}
