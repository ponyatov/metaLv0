
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
import django
django.setup()
from django.contrib.auth.models import User
# / <section:top>
# \ <section:mid>
su = User.objects.create_superuser(
	username='dponyatov',
	email='dponyatov@gmail.com',
	password='passwd'
)
su.save()
# / <section:mid>
# \ <section:bot>
# / <section:bot>