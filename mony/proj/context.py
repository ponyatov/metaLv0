
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
from django.contrib.auth.models import User
# / <section:top>
# \ <section:mid>
from app.apps import AppConfig
def title(request):
	return {'title':AppConfig.verbose_name}

def user(request):
	try:
		user = User.objects.get(id=request.user.id)
	except User.DoesNotExist:
		user = None
	return {'user':user}
# / <section:mid>
# \ <section:bot>
# / <section:bot>