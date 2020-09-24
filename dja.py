## @file
## @brief Django Apps Generator

from metaL import *
import config

## @defgroup dja dja
## @ingroup web
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
        return (S(f'def {self.val}(request): # {self}') //
                f"template = loader.get_template('{self.val}.html')" //
                "context = {}" //
                Return(f"HttpResponse(template.render(context, request))"))

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
class djModule(webModule):

    ## intercept `A[key]=B` operations
    def __setitem__(self, key, that):
        super().__setitem__(key, that)
        if isinstance(that, Title):
            self.init_app()

    def __init__(self, V=None):
        super().__init__(V)
        # routes
        self.index = djRoute('index')
        self.admin = djRoute('admin')
        # proj
        self.init_proj()
        # app
        self.init_app()
        # fixture
        self.init_fixture()

    def init_apt(self):
        super().init_apt()
        (self.apt // 'gdal-bin' // 'libspatialite7').sync()

    def init_config(self):
        super().init_config()
        self.mk.runserver // f'.PHONY: runserver\nrunserver: $(PY) manage.py\n\t$^ $@ {self.host}:{self.port}'
        self.mk.sync()
        return self.config.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.bot //\
            '/*.sqlite3' //\
            f'/{self.val}z/' //\
            '/dumpdata'
        return self.giti.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext // '"batisteo.vscode-django",' // '"randomfractalsinc.geo-data-viewer",'
        return self.vscode.ext.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        settings = self.vscode.settings
        #
        self.f11.cmd.val = 'make runserver'
        self.f12.cmd.val = 'make wasm'
        #
        self.vscode.assoc //\
            '"**/templates/**/*.html": "django-html",' //\
            '"**/templates/**/*": "django-txt",'
        #
        return settings.sync()

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
        return self.vscode.launch.sync()

    def vs_django(self, target, group='django'):
        return self.vs_make(target, group)

    def init_vscode_tasks(self):
        pyModule.init_vscode_tasks(self)
        self.tasks.it //\
            self.vs_django('migrate') //\
            self.vs_django('makemigrations') //\
            self.vs_django('dumpdata') //\
            self.vs_django('loaddata') //\
            ''
        return self.tasks.sync()

    def init_mk(self):
        super().init_mk()
        # src
        self.mk.src.dropall()
        files = {
            '': ['manage'],
            'proj/': ['context', 'settings', 'urls'],
            'app/': ['admin', 'apps', 'forms', 'models', 'views'],
        }
        for i in files:
            for j in files[i]:
                self.mk.src // f'SRC += {i}{j}.py'
        # all
        self.mk.all.dropall() //\
            '.PHONY: all' //\
            (S('all: $(PY) manage.py') // '$^')
        # install
        self.mk.install //\
            'ln -fs  ../../world/location.json fixture/location.json' //\
            '$(MAKE) js' //\
            '$(MAKE) migrate' //\
            '$(MAKE) createsuperuser' //\
            '$(MAKE) loaddata'
        # runserver
        self.mk.runserver = Section('runserver')
        self.mk.mid // self.mk.runserver
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
        # dumpdata
        dumpdata = Section('dumpdata')
        self.mk.mid // dumpdata
        dumpdata //\
            '.PHONY: dumpdata' //\
            (S('dumpdata: $(PY) manage.py') // '$^ dumpdata --indent 2 -o $@')
        # loaddata
        loaddata = Section('loaddata')
        self.mk.mid // loaddata
        loaddata //\
            '.PHONY: loaddata' //\
            (S('loaddata: $(PY) manage.py') //
             '$^ loaddata user.json location.json')
        #
        return self.mk.sync()

    def init_fixture(self):
        self['fixture'] = self.fixture = Dir('fixture')
        self.diroot // self.fixture
        self.fixture.sync()
        #
        self.fixture['user'] = self.fixture.user = File(
            'user.json', comment=None)
        self.fixture // self.fixture.user
        self.fixture.user.top // '['
        self.fixture.user.bot // ']'

        now = '2020-11-11T11:11:11.11'

        dponyatov = (S('{', '},') //
                     '"model": "app.customuser",' //
                     '"pk": 1,' //
                     (S('"fields": {', '}') //
                      f'"username": "{config.ADMIN.USERNAME}",' //
                      f'"password": "{config.ADMIN.PASS_HASH}",' //
                      f'"last_name": "{config.ADMIN.LAST}",' //
                      f'"first_name": "{config.ADMIN.FIRST}",' //
                      f'"father_name": "{config.ADMIN.FATHER}",' //
                      f'"email": "{config.ADMIN.EMAIL}",' //
                      f'"phone": "{config.ADMIN.PHONE}",' //
                      f'"loc": 3,' //
                      f'"date_joined": "{now}",' //
                      f'"last_login": "{now}",' //
                      '"is_superuser": true,' //
                      '"is_staff": true,' //
                      '"is_active": true,' //
                      '"groups": [],' //
                      '"user_permissions": []'))
        admin = (S('{', '}') //
                 '"model": "app.customuser",' //
                 '"pk": 2,' //
                 (S('"fields": {', '}') //
                  f'"username": "admin",' //
                  f'"password": "{config.ADMIN.PASS_HASH}",' //
                  f'"last_name": "Админов",' //
                  f'"first_name": "Админ",' //
                  f'"father_name": "Админович",' //
                  f'"email": "{config.ADMIN.EMAIL}",' //
                  f'"phone": "{config.ADMIN.PHONE}",' //
                  f'"loc": 3,' //
                  f'"date_joined": "{now}",' //
                  f'"last_login": "{now}",' //
                  '"is_superuser": true,' //
                  '"is_staff": true,' //
                  '"is_active": true,' //
                  '"groups": [],' //
                  '"user_permissions": []'))

        samara = ''#(S('{', '},') // '')

        self.fixture.user.mid // dponyatov // admin // samara
        self.fixture.user.sync()

        #
        return self.fixture

    def init_reqs(self):
        super().init_reqs()
        self.reqs // 'Django'
        return self.reqs.sync()

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
        return giti.sync()

    def init_proj_context(self):
        self.proj['context'] = self.proj.context = pyFile('context')
        self.proj // self.proj.context
        self.proj.context.mid // (Section('title') //
                                  "from app.apps import AppConfig" //
                                  (S("def title(request):") //
                                   "return {'title':AppConfig.verbose_name}"))
        self.proj.context.mid // (Section('date') //
                                  'from datetime import date as dt' //
                                  'from django.utils.formats import date_format' //
                                  (S('def date(request):') //
                                   'today = dt.today()' //
                                   "dateshort = date_format(today, format='SHORT_DATE_FORMAT', use_l10n=True)" //
                                   "datelong = date_format(today, format='DATE_FORMAT', use_l10n=True)" //
                                   'return {"dateshort":dateshort,"datelong":datelong}'))
        self.proj.context.mid // (Section('user') //
                                  (S('def user(request):') //
                                   (S('try:') //
                                    "user = request.user" //
                                    "try: f = user.last_name" //
                                    "except: f='?'" //
                                    "try: i = user.first_name[0]" //
                                    "except: i='?'" //
                                    "try: o = user.father_name[0]" //
                                    "except: o = '?'" //
                                    "user.shorten = f'{f} {i}.{o}.'"
                                    ) //
                                   (S("except CustomUser.DoesNotExist:") //
                                    "user = None"
                                    ) //
                                   "return {'user':user}"
                                   ))
        self.proj.context.mid // (Section('loc') //
                                  (S('def loc(request):') //
                                  'try: loc = request.user.loc'//
                                  'except AttributeError: loc = "???"'//
                                   'return {"loc":loc} '))
        return self.proj.context.sync()

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
                    "'loc'," //
                    "'last_name','first_name','father_name'," //
                    "'email','phone'," //
                    "'is_active','is_superuser'" //
                    ")") //
                (S('fieldsets = (') //
                    "(None,{'fields':('username','password')})," //
                    "(None,{'fields':('loc',)})," //
                    "(None,{'classes': ('wide',),'fields':('last_name','first_name','father_name')})," //
                    "(None,{'fields':('email','phone')})," //
                    "(None,{'fields':('is_staff', 'is_active')})," //
                    ')') //
                ''
             ) //\
            'admin.site.register(CustomUser,CustomUserAdmin)'
        # (S( + (") //\
        #     "(None, {'fields': [fldz]})," //\
        return self.app.admin.sync()

    def init_app_models(self):
        self.app['models'] = self.app.models = pyFile('models')
        self.app // self.app.models
        self.app.models.top //\
            '# https://tproger.ru/translations/extending-django-user-model/#var2' //\
            "from django.db import models" //\
            '# Django GIS' //\
            'from django.contrib.gis.db import models as gismodels'
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
            (S("class CustomUser(AbstractUser): # AbstractBaseUser") //
                "father_name = models.CharField('отчество', max_length=0x22, null=True, blank=True)" //
                "phone = models.CharField('телефон',max_length=0x11, null=True, blank=True)" //
                "loc = models.ForeignKey('Location', on_delete=models.DO_NOTHING, null=True, blank=True)"
             )
#         # "\tUSERNAME_FIELD = 'username'" //\
#         # "\tREQUIRED_FIELDS = ['email']" //\
#         # "\tobjects = CustomUserManager()" //\
#         # "\tdef __str__(self): return '%s %s' % (self.username, self.email)" //\
        #
        location = Section('location')
        self.app.models.mid // location
        location // (S('class Location(gismodels.Model):') //
                     "name = models.CharField('название', max_length=0x22, blank=False)" //
                     "shape = gismodels.PolygonField('границы', null=True, blank=True)" //
                     (S("class Meta:") //
                      "verbose_name = 'регион'" //
                      "verbose_name_plural = 'регионы'" //
                      "ordering = ['name']") //
                     (S("def __str__(self):") //
                      "return '%s'%self.name")
                     )
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
        return self.app.admin.sync()

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
        return self.app.forms.sync()

    # def init_templates(self):
    #     super().init_templates()
    #     # self['templates'] = self.templates = Dir('templates')
    #     # self.diroot // self.templates
    #     # self.templates.sync()
    #     # self.templates // File('.gitignore')
    #     # self.init_templates_all()
    #     # self.init_templates_index()
    #     # self.init_templates_admin()

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
        return base_site.sync()

    def static_url(self, filename):
        return '{%% static "%s" %%}' % filename

    def init_templates_all(self):
        super().init_templates_all()
        self.templates.all.jinja //\
            '{% load static %}'
        return self.templates.all.sync()

    def init_templates_index(self):
        super().init_templates_index()
        self.templates['index'] = self.templates.index = File(
            'index.html', comment='<!--')
        self.templates // self.templates.index
        self.templates.index.top // "{% extends 'all.html' %}"
        self.templates.index.top // "{% load static %}" // ''
        return self.templates.index.sync()

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
        self.proj.settings.top // 'import config'
        self.proj.settings.top // 'from pathlib import Path'
        self.proj.settings.top // 'BASE_DIR = Path(__file__).resolve(strict=True).parent.parent'
        self.proj.settings.top // pyImport('os')
        self.proj.settings.top // 'SECRET_KEY = config.SECRET_KEY'
        self.proj.settings.mid // 'DEBUG = True'
        self.proj.settings.mid // 'ALLOWED_HOSTS = []'
        self.init_proj_installed()
        self.proj.settings.mid // "AUTH_USER_MODEL = 'app.CustomUser'"
        self.init_proj_middleware()
        self.proj.settings.mid //\
            "ROOT_URLCONF = 'proj.urls'" //\
            "FIXTURE_DIRS = [BASE_DIR/'fixture']"
        self.init_proj_templates()
        self.init_proj_databases()
        self.init_proj_i18n()
        self.init_proj_static()
        self.proj.settings.sync()
        self.mk.sync()

    def init_proj_installed(self):
        self.proj['installed'] = self.proj.installed = Section('installed')
        self.proj.settings.mid // (
            S('INSTALLED_APPS = [', ']') // self.proj.installed)
        self.proj.installed //\
            "'django.contrib.admin'," //\
            "'django.contrib.auth'," //\
            "'django.contrib.contenttypes'," //\
            "'django.contrib.sessions'," //\
            "'django.contrib.messages'," //\
            "'django.contrib.staticfiles'," //\
            "'django.contrib.gis'," //\
            "'app',"

    def init_proj_middleware(self):
        self.proj['middleware'] = self.proj.middleware = Section('middleware')
        self.proj.settings.mid // (
            S('MIDDLEWARE = [', ']') // self.proj.middleware)
        # self.proj.middleware // "\t'django.middleware.security.SecurityMiddleware',"
        self.proj.middleware //\
            "'django.contrib.sessions.middleware.SessionMiddleware'," //\
            "'django.contrib.auth.middleware.AuthenticationMiddleware'," //\
            "'django.contrib.messages.middleware.MessageMiddleware',"

    def init_proj_templates(self):
        self.proj['templates'] = self.proj.templates = Section('templates')
        self.proj.settings.mid // (
            S('TEMPLATES = [', ']') // self.proj.templates)
        self.proj.context = S('', '')
        for ctx in ['user', 'loc', 'date', 'title']:
            self.proj.context // f"'proj.context.{ctx}',"
        self.proj.templates //\
            (S('{', '},') //
             "'BACKEND': 'django.template.backends.django.DjangoTemplates'," //
             "'DIRS': [BASE_DIR/'templates'], # req for /template resolve" //
             "'APP_DIRS': True, # req for admin/login.html template" //
             (S("'OPTIONS': {", "}") //
              (S("'context_processors': [", "],") //
               "'django.template.context_processors.debug'," //
               "'django.template.context_processors.request'," //
               "'django.contrib.auth.context_processors.auth'," //
               "'django.contrib.messages.context_processors.messages'," //
               self.proj.context
               )
              ))

    def init_proj_databases(self):
        self.proj['databases'] = self.proj.databases = Section('databases')
        self.proj.settings.mid // (
            S("DATABASES = {", "}") // self.proj.databases)
        self.proj.databases //\
            (S("'default': {", "}") //
             (S("'ENGINE': 'django.contrib.gis.db.backends.spatialite',") //
              ("'NAME': BASE_DIR/'%s.sqlite3'," % self.val))
             )
        #  (S("'ENGINE': 'django.db.backends.sqlite3',") //

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
            "from django.template import loader" //\
            "from .models import *"
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
