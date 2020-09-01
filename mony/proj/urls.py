
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
## @brief URL routing
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
# / <section:top>
# \ <section:mid>
	path('', views.index, name='index'),
	path('admin/', admin.site.urls, name='admin'),
# / <section:mid>
# \ <section:bot>
]
# / <section:bot>