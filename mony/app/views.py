
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
from django.http import HttpResponse
from django.template import loader
# / <section:top>
# \ <section:mid>

def index(request): # <djroute:index>
	template = loader.get_template('index.html')
	context = {}
	return HttpResponse(template.render(context, request))
# / <section:mid>
# \ <section:bot>
# / <section:bot>