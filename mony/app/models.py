
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
# https://tproger.ru/translations/extending-django-user-model/#var2
from django.db import models
# / <section:top>
# \ <section:mid>

# \ <section:user>
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser):
	pass
# / <section:user>

# \ <section:location>
class Location(models.Model):
	name = models.CharField('название', max_length=0x22, blank=False)
	class Meta:
		verbose_name = 'регион'
		verbose_name_plural = 'регионы'
	def __str__(self):
		return '%s'%self.name
# / <section:location>
# / <section:mid>
# \ <section:bot>
# / <section:bot>