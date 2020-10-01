#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
# / <section:top>
# \ <section:mid>
def index(request): # index
    template = loader.get_template('index.html')
    context = {}
    if request.user.is_authenticated:
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseRedirect(f'/admin/login/?next={request.path}')
# / <section:mid>
