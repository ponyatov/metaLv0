
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
import config
# / <section:top>
# \ <section:mid>


import sys, re, shapefile

json = 'location.json'

if sys.argv[1] == '[':
    open(json, 'w').write("[")
    sys.exit(0)
if sys.argv[1] == ']':
    with open(json, 'a') as a:
        a.seek(0,2)
        a.truncate(a.tell()-1)
        a.write("\n]\n")
    sys.exit(0)

name = sys.argv[1]
assert re.match(r'^[A-Z][a-z]+\.shp$', name)

with open(json, 'a') as j:
    with shapefile.Reader(name) as shp:
        print(f'shp: {name}')
        feature = shp.shapeRecords()[0]
        print(f'feature: {feature}')
        first = feature.shape.__geo_interface__
        dat = first['coordinates'][0]
        dat = ', '.join(f'{i[0]} {i[1]}' for i in dat)
        dat = dat
        j.write("""
{
	"model": "app.location",
	"pk": %s,
	"fields": {
		"name":  "%s",
        "shape": "SRID=4326;POLYGON ((%s))"
	}
},""" % (sys.argv[3], sys.argv[2], dat))


# / <section:mid>