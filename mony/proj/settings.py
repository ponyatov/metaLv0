
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
## @brief Django settings
from pathlib import Path
import os
# / <section:top>
# \ <section:mid>
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = "abcdefgh"#"os.urandom(64)"
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
TEMPLATES = [

# \ <section:templates>
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [BASE_DIR/'templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'proj.context.user', 'proj.context.title', 
			],
		},
	},
# / <section:templates>
]
DATABASES = {

# \ <section:databases>
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR/'mony.sqlite3',
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
# \ <section:bot>
# / <section:bot>