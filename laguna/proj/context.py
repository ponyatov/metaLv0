#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:mid>
# \ <section:title>
from app.apps import AppConfig
def title(request):
    return {'title':AppConfig.verbose_name}
# / <section:title>
# \ <section:date>
from datetime import date as dt
from django.utils.formats import date_format
def date(request):
    today = dt.today()
    dateshort = date_format(today, format='SHORT_DATE_FORMAT', use_l10n=True)
    datelong = date_format(today, format='DATE_FORMAT', use_l10n=True)
    return {"dateshort":dateshort,"datelong":datelong}
# / <section:date>
# \ <section:user>
def user(request):
    try:
        user = request.user
        try: f = user.last_name
        except: f='?'
        try: i = user.first_name[0]
        except: i='?'
        try: o = user.father_name[0]
        except: o = '?'
        user.shorten = f'{f} {i}.{o}.'
    except CustomUser.DoesNotExist:
        user = None
    return {'user':user}
# / <section:user>
# \ <section:loc>
def loc(request):
    try: loc = request.user.loc
    except AttributeError: loc = "???"
    return {"loc":loc} 
# / <section:loc>
# / <section:mid>
