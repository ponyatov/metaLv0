#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
# https://tproger.ru/translations/extending-django-user-model/#var2
from django.db import models
# Django GIS
from django.contrib.gis.db import models as gismodels
# / <section:top>
# \ <section:mid>
# \ <section:validators>
from django.core import validators
valPhone = validators.RegexValidator(r"^\+7 \d{3} \d{2} \d{2} \d{3}$", message="+7 ??? ?? ?? ???")
valOKATO = validators.RegexValidator(r"^(36|53)\d{9}$", message="ОКАТО: 11 цифр")
valKLADR = validators.RegexValidator(r"^(63|56)\d{11,15}$", message="КЛАДР: 13..17 цифр")

# / <section:validators>
# \ <section:manager>
from django.contrib.auth.base_user import BaseUserManager

## extended user model
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        assert extra_fields.get('is_staff')
        assert extra_fields.get('is_superuser')
        return self.create_user(username=username, email=email, password=password, **extra_fields)
# / <section:manager>
# \ <section:user>
from django.contrib.auth.models import AbstractUser
class CustomUser(AbstractUser): # AbstractBaseUser
    father_name = models.CharField('отчество', max_length=0x22, null=True, blank=True)
    phone = models.CharField('телефон', max_length=0x11, null=True, blank=True, validators=[valPhone])
    loc = models.ForeignKey('Location',verbose_name='регион',
        on_delete=models.DO_NOTHING, null=True, blank=True,
        limit_choices_to={'userbind':True})
# / <section:user>
# \ <section:location>
class Location(gismodels.Model):
    name = models.CharField('название', max_length=0x22, blank=False, unique=True)
    okato = models.CharField('ОКАТО', max_length=11, null=True, blank=True, validators=[valOKATO])
    kladr = models.CharField('КЛАДР', max_length=17, null=True, blank=True, validators=[valKLADR])
    shape = gismodels.PolygonField('границы', null=True, blank=True)
    userbind = models.BooleanField('привязка пользователей', default=False)
    class Meta:
        verbose_name = 'регион'
        verbose_name_plural = 'регионы'
        ordering = ['-userbind','name']
    def __str__(self):
        return f'{self.name}'
# / <section:location>
# / <section:mid>
