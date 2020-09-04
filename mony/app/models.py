
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
# https://tproger.ru/translations/extending-django-user-model/#var2
from django.db import models
# / <section:top>
# \ <section:mid>

# \ <section:user>
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser): # AbstractBaseUser
	pass
# / <section:user>

# \ <section:manager>
from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
	def create_user(self, username, email=None, password=None, **extra_fields):
		# user = self.model(email=email, **extra_fields)
		user = CustomUser.objects.create_user(
			username, email, password,
			first_name = 'Dmitry', last_name = 'Ponyatov'
		)
		user.set_password(password)
		user.save()
		return user
	def create_superuser(self, username, email=None, password=None, **extra_fields):
		assert extra_fields.get('is_staff')
		assert extra_fields.get('is_superuser')
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		extra_fields.setdefault('is_active', True)
		return self.create_user(username, email=None, password=None, **extra_fields)

# / <section:manager>

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