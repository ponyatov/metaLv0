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

# ## plugin
# ## @ingroup dja
# class djPlugin(DJ, Module):
#     pass


# ## @ingroup dja
# ## `GeoDjango` GIS subsystem
# ## * https://krzysztofzuraw.com/blog/2016/geodjango-leaflet-part-one.html
# ## * https://krzysztofzuraw.com/blog/2016/geodjango-leaflet-part-two.html
# geodjango = djPlugin('geodjango')

## Django minimal project
## @ingroup dja
class djModule(DJ, pyModule):

    ## intercept `A[key]=B` operations
    def __setitem__(self, key, that):
        super().__setitem__(key, that)
        if isinstance(that, Title):
            self.init_app()

    def __init__(self, V=None):
        pyModule.__init__(self, V)
        # routes
        self.index = djRoute('index')
        self.admin = djRoute('admin')
        # templates
        self.init_templates()
        # static
        self.init_static()
        # proj
        self.init_proj()
        # app
        self.init_app()

#         # # manage.py
#         # self.init_manage()
#         # # setup.py
#         # self.init_install()
#         # # tasks
#         # self.init_tasks()
#         # # templates
#         # self.init_templates()
#         # # admin
#         # self.init_admin()
#         # # models
#         # self.init_models()
#         # # forms
#         # self.init_forms()

    def init_settings(self):
        pyModule.init_settings(self)
        self.settings.f11 // 'make runserver'
        self.settings.f12 // 'make check'
        self.settings.sync()

    def init_vscode_tasks(self):
        pyModule.init_vscode_tasks(self)
        self.tasks.it //\
            (S('{') //
                '"label": "Django: migrate",' //
                '"type": "shell",' //
                '"command": "make migrate",' //
                '"problemMatcher": []' //
                '},')
        self.tasks.it //\
            (S('{') //
                '"label": "Django: makemigrations",' //
                '"type": "shell",' //
                '"command": "make makemigrations",' //
                '"problemMatcher": []' //
                '},')
        self.tasks.sync()

    def init_vscode_launch(self):
        super().init_vscode_launch()
        self.vscode.launch.program.dropall() //\
            '"program": "manage.py",' //\
            '"django": true,'
        self.vscode.launch.args //\
            '"runserver", "--no-color", "--noreload", "--nothreading"'
        self.vscode.launch.opts //\
            '"WaitOnAbnormalExit", "WaitOnNormalExit",' //\
            '"RedirectOutput", "DjangoDebugging"'
        self.vscode.launch.sync()

    def init_reqs(self):
        super().init_reqs()
        self.reqs // 'django'
        self.reqs.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.bot // '/*.sqlite3'
        self.giti.bot // ('/%sz/' % self.val)
        self.giti.sync()

    def init_mk(self):
        pyModule.init_mk(self)
        # src
        self.mk.src.dropall()
        self.mk.src //\
            'SRC += manage.py' //\
            'SRC += app/models.py' //\
            'SRC += app/apps.py' //\
            'SRC += app/settings.py' //\
            'SRC += proj/urls.py' //\
            ''
        # all
        self.mk.all // '.PHONY: all\nall: $(PY) manage.py\n\t$^'
        # install
        self.mk.install //\
            '\t$(MAKE) js' //\
            '\t$(MAKE) migrate' //\
            '\t$(MAKE) createsuperuser'
        # js
        js = Section('js/install')
        self.mk.update.after(js)
        js //\
            ".PHONY: js" //\
            "js: static/jquery.js static/bootstrap.css static/bootstrap.js" //\
            '' //\
            "JQUERY_VER = 3.5.0" //\
            "static/jquery.js:" //\
            "\t$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js" //\
            '' //\
            "BOOTSTRAP_VER = 3.4.1" //\
            "BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/" //\
            "static/bootstrap.css:" //\
            "\t$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css" //\
            "static/bootstrap.js:" //\
            "\t$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js"
        js.sync()
        # runserver
        runserver = Section('runserver')
        self.mk.mid // runserver
        runserver // '.PHONY: runserver\nrunserver: $(PY) manage.py\n\t$^ $@'
        # check
        check = Section('check')
        self.mk.mid // check
        check // '.PHONY: check\ncheck: $(PY) manage.py\n\t$^ $@'
        # makemigrations
        makemigrations = Section('makemigrations')
        self.mk.mid // makemigrations
        makemigrations // '.PHONY: makemigrations\nmakemigrations: $(PY) manage.py\n\t$^ $@ app'
        # migrate
        migrate = Section('migrate')
        self.mk.mid // migrate
        migrate //\
            '.PHONY: migrate\nmigrate: $(PY) manage.py' //\
            '\t$(MAKE) makemigrations' //\
            '\t$^ $@'
        # createsuperuser
        createsuperuser = Section('createsuperuser')
        self.mk.mid // createsuperuser
        createsuperuser //\
            '.PHONY: createsuperuser\ncreatesuperuser: $(PY) manage.py' //\
            '\t$^ $@ \\' //\
            ('\t\t--username %s \\' % self['EMAIL'].val.split('@')[0]) //\
            ('\t\t--email %s' % self['EMAIL'].val)
        self.mk.sync()

    def init_py(self):
        pass

    def init_app_migrations(self):
        self['migrations'] = self.migrations = Dir('migrations')
        self.app // self.migrations
        self.migrations.sync()
        self.migrations // File('__init__.py').sync()
        giti = File('.gitignore', comment=None)
        self.migrations // giti
        giti // '????_*.py'
        giti.sync()
#         # self.migrations.user = pyFile('0000_initial')
#         # self.migrations // self.migrations.user
#         # self.migrations.user.top // "from django.conf import settings"
#         # self.migrations.user.top // "from django.db import migrations, models"
#         # self.migrations.user.mid // "class Migration(migrations.Migration):"
#         # self.migrations.user.mid // "\tdependencies = ["
#         # self.migrations.user.mid // "\t\tmigrations.swappable_dependency(settings.AUTH_USER_MODEL),"
#         # self.migrations.user.mid // "\t]"
#         # self.migrations.user.mid // "\toperations = ["
#         # self.migrations.user.mid // "\t]"
#         # self.migrations.user.sync()

#     def init_install(self):
#         self.diroot['install'] = self.proj.install = pyFile('install')
#         self.diroot // self.proj.install
#         self.proj.install.top //\
#             'import os' //\
#             'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")' //\
#             'import django' //\
#             'django.setup()' //\
#             'from django.contrib.auth.models import User'
#         self.proj.install.mid //\
#             'su = User.objects.create_superuser(' //\
#             "\tusername='dponyatov'," //\
#             "\temail='dponyatov@gmail.com'," //\
#             "\tpassword='passwd'" //\
#             ')' //\
#             'su.save()'
#         self.proj.install.sync()
#         # self.mk.install // '\t$(PY) install.py'
#         self.mk.sync()

    def init_proj_context(self):
        self.proj['context'] = self.proj.context = pyFile('context')
        self.proj // self.proj.context
        self.proj.context.mid //\
            "from app.apps import AppConfig" //\
            "def title(request):" //\
            "\treturn {'title':AppConfig.verbose_name}" //\
            ''
        self.proj.context.mid //\
            'from app.models import CustomUser' //\
            'def user(request):' //\
            '\ttry:' //\
            "\t\tuser = CustomUser.objects.get(id=request.user.id)" //\
            "\t\ttry: f = user.last_name" //\
            "\t\texcept: f=''" //\
            "\t\ttry: i = user.first_name[0]" //\
            "\t\texcept: i=''" //\
            "\t\ttry: o = user.father_name[0]" //\
            "\t\texcept: o = ''" //\
            "\t\tuser.shorten = '%s %s.%s.'%(f,i,o)" //\
            "\texcept CustomUser.DoesNotExist:" //\
            "\t\tuser = None" //\
            "\treturn {'user':user}" //\
            self.proj.context.sync()

    def init_app_admin(self):
        self.app['admin'] = self.app.admin = pyFile('admin')
        self.app // self.app.admin
        self.app.admin.top //\
            'from django.contrib import admin' //\
            'from .models import *'
        #
        self.app.admin.mid //\
            "from django.contrib.auth.admin import UserAdmin" //\
            "from .forms import CustomUserCreationForm, CustomUserChangeForm" //\
            (S("class CustomUserAdmin(UserAdmin):") //
                "add_form = CustomUserCreationForm" //
                "form = CustomUserChangeForm" //
                "model = CustomUser" //
                (S("list_display = (") //
                    "'username'," //
                    "'last_name','first_name','father_name'," //
                    "'email','phone'," //
                    "'is_active','is_superuser'" //
                    ")") //
                (S('fieldsets = (') //
                    "(None,{'fields':('username','password')})," //
                    "(None,{'classes': ('wide',),'fields':('last_name','first_name','father_name')})," //
                    "(None,{'fields':('email','phone')})," //
                    "(None,{'fields':('is_staff', 'is_active')})," //
                    ')') //
                ''
             ) //\
            'admin.site.register(CustomUser,CustomUserAdmin)'
        # (S( + (") //\
        #     "(None, {'fields': [fldz]})," //\
        self.app.admin.sync()

    def init_app_models(self):
        self.app['models'] = self.app.models = pyFile('models')
        self.app // self.app.models
        self.app.models.top //\
            '# https://tproger.ru/translations/extending-django-user-model/#var2' //\
            "from django.db import models"
        # https://webdevblog.ru/sovremennyj-sposob-sozdanie-polzovatelskoj-modeli-user-v-django/
        # https://habr.com/ru/post/313764/
        # https://testdriven.io/blog/django-custom-user-model/
        #
        manager = Section('manager')
        self.app.models.mid // manager
        manager //\
            "from django.contrib.auth.base_user import BaseUserManager" //\
            "class CustomUserManager(BaseUserManager):" //\
            "\tdef create_user(self, username, email=None, password=None, **extra_fields):" //\
            "\t\tuser = self.model(username=username, email=email, **extra_fields)" //\
            "\t\tuser.set_password(password)" //\
            "\t\tuser.save()" //\
            "\t\treturn user" //\
            "\tdef create_superuser(self, username, email=None, password=None, **extra_fields):" //\
            "\t\textra_fields.setdefault('is_staff', True)" //\
            "\t\textra_fields.setdefault('is_superuser', True)" //\
            "\t\textra_fields.setdefault('is_active', True)" //\
            "\t\tassert extra_fields.get('is_staff')" //\
            "\t\tassert extra_fields.get('is_superuser')" //\
            "\t\treturn self.create_user(username=username, email=email, password=password, **extra_fields)" //\
            ''
#         #     "\t\tuser = CustomUser.objects.create_user(" //\
#         #     "\t\t\tusername, email, password," //\
#         #     "\t\t\tfirst_name = 'Dmitry', last_name = 'Ponyatov'" //\
        #
        user = Section('user')
        self.app.models.mid // user
        user //\
            "from django.contrib.auth.models import AbstractUser" //\
            "class CustomUser(AbstractUser): # AbstractBaseUser" //\
            "\tfather_name = models.CharField('отчество', max_length=0x22, null=True, blank=True)" //\
            "\tphone = models.CharField('телефон',max_length=0x11,null=True, blank=True)"
#         # "\tUSERNAME_FIELD = 'username'" //\
#         # "\tREQUIRED_FIELDS = ['email']" //\
#         # "\tobjects = CustomUserManager()" //\
#         # "\tdef __str__(self): return '%s %s' % (self.username, self.email)" //\
        #
        location = Section('location')
        self.app.models.mid // location
        location // 'class Location(models.Model):' //\
            "\tname = models.CharField('название', max_length=0x22, blank=False)" //\
            "\tclass Meta:" //\
            "\t\tverbose_name = 'регион'" //\
            "\t\tverbose_name_plural = 'регионы'" //\
            "\tdef __str__(self):" //\
            "\t\treturn '%s'%self.name"
        self.app.admin.bot // 'admin.site.register(Location)'
#         # profile = Section('profile')
#         # self.models.mid // profile
#         # self.proj.admin.bot // 'admin.site.register(Profile)'
#         # profile // "class Profile(models.Model):" //\
#         # "from django.contrib.auth.models import User"//\
#         #     "\tuser = models.OneToOneField(User, verbose_name='пользователь', on_delete=models.CASCADE)" //\
#         #     "\tloc = models.ForeignKey(Location, verbose_name='регион', on_delete=models.DO_NOTHING)" //\
#         #     "\tphone = models.CharField('телефон',max_length=0x11,blank=True)" //\
#         #     "\tclass Meta:" //\
#         #     "\t\tverbose_name = 'профиль пользователя'" //\
#         #     "\t\tverbose_name_plural = 'профили пользователей'" //\
#         #     "\tdef __str__(self):" //\
#         #     "\t\treturn '%s @ %s | %s'%(self.user,self.loc,self.phone)"
        self.app.models.sync()
        self.app.admin.sync()

    def init_app_forms(self):
        self.app['forms'] = self.app.forms = pyFile('forms')
        self.app // self.app.forms
        meta = '' +\
            "\tclass Meta(UserCreationForm):" +\
            "\n\t\tmodel = CustomUser" +\
            "\n\t\tfields = '__all__'"
        self.app.forms.mid //\
            "from django.contrib.auth.forms import UserCreationForm, UserChangeForm" //\
            "from .models import CustomUser" //\
            "class CustomUserCreationForm(UserCreationForm):" // meta //\
            "class CustomUserChangeForm(UserChangeForm):" // meta //\
            ''
        self.app.forms.sync()

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
        self.init_templates_admin()

    def init_templates_admin(self):
        admin = Dir('admin')
        self.templates // admin
        admin.sync()
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
        self.templates.all //\
            '{% load static %}' //\
            '<!DOCTYPE html>' //\
            '<html lang="ru">'
        self.templates.all //\
            '\t<head>' //\
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
        self.templates.all //\
            '\t<body>' //\
            '\t\t{% block body %}{% endblock %}' //\
            '\t\t<script src="{% static "jquery.js" %}"></script>' //\
            '\t\t<script src="{% static "bootstrap.js" %}"></script>' //\
            '\t</body>'
        self.templates.all //\
            '</html>'
        self.templates.all.sync()

    def init_templates_index(self):
        self.templates['index'] = self.templates.index = File(
            'index.html', comment=None)
        self.templates // self.templates.index
        self.templates.index.top // "{% extends 'all.html' %}"
        self.templates.index.top // "{% load static %}" // ''
        self.templates.index.sync()

    def init_proj(self):
        self['proj'] = self.proj = Dir('proj')
        self.diroot // self.proj
        self.proj.sync()
        self.proj // pyFile('__init__')
        self.init_proj_settings()
        self.init_proj_urls()
        self.init_proj_context()

    def init_app(self):
        self['app'] = self.app = Dir('app')
        self.diroot // self.app
        self.app.sync()
        self.app // pyFile('__init__')
        self.init_app_apps()
        self.init_app_views()
        self.init_app_forms()
        self.init_app_admin()
        self.init_app_models()
        self.init_app_migrations()

    def init_app_apps(self):
        self.app['apps'] = self.app.apps = pyFile('apps')
        self.app // self.app.apps
        self.app.apps.top //\
            'from django.apps import AppConfig'
        try:
            title = self['TITLE'].val
        except KeyError:
            title = self.val
        self.app.apps.mid //\
            "class AppConfig(AppConfig):" //\
            "\tname = 'app'" //\
            ("\tverbose_name = '%s'" % title)
        self.app.apps.sync()

    def init_proj_settings(self):
        self.proj['settings'] = self.proj.settings = pyFile('settings')
        self.proj // self.proj.settings
        self.proj.settings.top // '## @brief Django settings'
        self.proj.settings.top // 'from pathlib import Path'
        self.proj.settings.top // 'BASE_DIR = Path(__file__).resolve(strict=True).parent.parent'
        self.proj.settings.top // pyImport('os')
        self.proj.settings.top // 'SECRET_KEY = "os.urandom(64)"'
        self.proj.settings.mid // 'DEBUG = True'
        self.proj.settings.mid // 'ALLOWED_HOSTS = []'
        self.init_proj_installed()
        self.proj.settings.mid // "AUTH_USER_MODEL = 'app.CustomUser'"
        self.init_proj_middleware()
        self.proj.settings.mid // "ROOT_URLCONF = 'proj.urls'"
        self.init_proj_templates()
        self.init_proj_databases()
        self.init_proj_i18n()
        self.init_proj_static()
        self.proj.settings.sync()
        self.mk.sync()

    def init_proj_installed(self):
        self.proj['installed'] = self.proj.installed = Section('installed')
        self.proj.settings.mid // 'INSTALLED_APPS = [' // self.proj.installed // ']'
        self.proj.installed //\
            "\t'django.contrib.admin'," //\
            "\t'django.contrib.auth'," //\
            "\t'django.contrib.contenttypes'," //\
            "\t'django.contrib.sessions'," //\
            "\t'django.contrib.messages'," //\
            "\t'django.contrib.staticfiles'," //\
            "\t'app',"

    def init_proj_middleware(self):
        self.proj['middleware'] = self.proj.middleware = Section('middleware')
        self.proj.settings.mid // 'MIDDLEWARE = [' // self.proj.middleware // ']'
        # self.proj.middleware // "\t'django.middleware.security.SecurityMiddleware',"
        self.proj.middleware // "\t'django.contrib.sessions.middleware.SessionMiddleware',"
        self.proj.middleware // "\t'django.contrib.auth.middleware.AuthenticationMiddleware',"
        self.proj.middleware // "\t'django.contrib.messages.middleware.MessageMiddleware',"

    def init_proj_templates(self):
        self.proj['templates'] = self.proj.templates = Section('templates')
        self.proj.settings.mid // 'TEMPLATES = [' // self.proj.templates // ']'
        self.proj.templates //\
            '\t{' //\
            "\t\t'BACKEND': 'django.template.backends.django.DjangoTemplates'," //\
            "\t\t'DIRS': [BASE_DIR/'templates'], # req for /template resolve" //\
            "\t\t'APP_DIRS': True, # req for admin/login.html template" //\
            "\t\t'OPTIONS': {" //\
            "\t\t\t'context_processors': [" //\
            "\t\t\t\t'django.template.context_processors.debug'," //\
            "\t\t\t\t'django.template.context_processors.request'," //\
            "\t\t\t\t'django.contrib.auth.context_processors.auth'," //\
            "\t\t\t\t'django.contrib.messages.context_processors.messages'," //\
            "\t\t\t\t'proj.context.user', 'proj.context.title', " //\
            '\t\t\t],' //\
            '\t\t},' //\
            '\t},'

    def init_proj_databases(self):
        self.proj['databases'] = self.proj.databases = Section('databases')
        self.proj.settings.mid // "DATABASES = {" // self.proj.databases // "}"
        self.proj.databases //\
            "\t'default': {" //\
            "\t\t'ENGINE': 'django.db.backends.sqlite3'," //\
            ("\t\t'NAME': BASE_DIR/'%s.sqlite3'," % self.val) //\
            "\t}"

    def init_proj_i18n(self):
        self.proj['i18n'] = self.proj.i18n = Section('i18n')
        self.proj.settings.mid // self.proj.i18n
        self.proj.i18n //\
            "LANGUAGE_CODE = 'ru-ru'"
        # "USE_I18N = True" //\
        # "USE_L10N = True" //\
        # "TIME_ZONE = 'UTC'" //\
        # "USE_TZ = True"

    def init_proj_static(self):
        static = Section('static')
        self.proj.settings.mid // static
        static //\
            "STATIC_URL = '/static/'" //\
            "STATICFILES_DIRS = [BASE_DIR/'static']"

    def init_app_views(self):
        self.app['views'] = self.app.views = pyFile('views')
        self.app // self.app.views
        self.app.views.top //\
            "from django.http import HttpResponse" //\
            "from django.template import loader"
        self.app.views.mid //\
            self.index.py_view()
        self.app.views.sync()

    def init_proj_urls(self):
        self.proj['urls'] = self.proj.urls = pyFile('urls')
        self.proj // self.proj.urls
        self.proj.urls.top //\
            'from django.contrib import admin' //\
            'from django.urls import path' // '' //\
            'from app import views' // '' //\
            'urlpatterns = ['
        self.proj.urls.mid //\
            self.index.py_url(route='') //\
            self.admin.py_url(request='admin.site.urls')
        self.proj.urls.bot //\
            ']'
        self.proj.urls.sync()

        # pyModule.init_py(self)
#         os.remove('%s/%s.py' % (self.diroot.val, self.diroot.val))
#         os.remove('%s/metaL.py' % self.diroot.val)
#         os.remove('%s/config.py' % self.diroot.val)
#         self.py.metal.dropall()
#         self.py.bot.dropall()
#         self.py.sync()

#     ## `.gitignore` callback from `anyModule.__init__()``
#     def init_gitignore(self):
#         pyModule.init_gitignore(self)
#         self.gitignore.mid // ("%s.sqlite3" % self.val)
#         self.gitignore.bot // ('/%sz/' % self.val)
#         self.gitignore.sync()

#     def init_manage(self):
#         self.manage = self['manage'] = pyFile('manage')
#         self.mksrc(self.manage)
#         self.diroot // self.manage
#         self.manage.top // ('## @file %s' % self.file())
#         self.manage.top // pyImport('os') // pyImport('sys')
#         self.manage.main = pyFn('main')
#         self.manage.main // (
#             "os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')")
#         self.manage.main // "from django.core.management import execute_from_command_line"
#         self.manage.main // "execute_from_command_line(sys.argv)"
#         self.manage.mid // self.manage.main
#         self.manage.bot // "if __name__ == '__main__':"
#         self.manage.bot // '\tmain()'
#         self.manage.sync()


# # MODULE = djModule('dja')

# # TITLE = Title('Generic Django App /metaL-templated/')
# # MODULE << TITLE

# # ABOUT = '''
# # Automatic (generative) programming approach to building intranet business systems:
# # * Python/Django/PostgreSQL stack
# # * powered by `metaL`
# # '''
# # MODULE['about'] = ABOUT

# # ## `~/metaL/$MODULE` target directory for code generation
# # diroot = MODULE['dir']

## @}
