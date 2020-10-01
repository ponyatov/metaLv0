#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
## @brief Django settings
import config
from pathlib import Path
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
import os
SECRET_KEY = config.SECRET_KEY
# / <section:top>
# \ <section:mid>
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    # \ <section:installed>
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'app',
    # / <section:installed>
]
AUTH_USER_MODEL = 'app.CustomUser'
MIDDLEWARE = [
    # \ <section:middleware>
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # / <section:middleware>
]
ROOT_URLCONF = 'proj.urls'
FIXTURE_DIRS = [BASE_DIR/'fixture']
TEMPLATES = [
    # \ <section:templates>
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'], # req for /template resolve
        'APP_DIRS': True, # req for admin/login.html template
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                
                    'proj.context.user',
                    'proj.context.loc',
                    'proj.context.date',
                    'proj.context.title',

            ],
        }
    },
    # / <section:templates>
]
DATABASES = {
    # \ <section:databases>
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
            'NAME': BASE_DIR/'laguna.sqlite3',
    }
    # / <section:databases>
}
# \ <section:i18n>
LANGUAGE_CODE = 'ru-ru'
# / <section:i18n>
# \ <section:static>
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR/'static']
# / <section:static>
# / <section:mid>
