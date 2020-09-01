
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
from django.contrib import admin
# / <section:top>
# \ <section:mid>
from .models import *
# / <section:mid>
# \ <section:bot>
admin.site.register(Location)
# / <section:bot>