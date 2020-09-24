## @file
## @brief shared GIS data

from metaL import *

## @defgroup world world
## @ingroup samples
## @brief shared GIS data
## @{

REGIONS = {
    'Orenburg': 'Оренбургская область',
    'Penza': 'Пензенская область',
    'Samara': 'Самарская область',
    'Saratov': 'Саратовская область',
    'Ulianovsk': 'Ульяновская область'
}


MODULE = minpyModule()
diroot = MODULE['dir']

MODULE['TITLE'] = TITLE = Title('shared GIS data')

MODULE['ABOUT'] = '''
scripts and GIS data dedicated from most other projects to make it a shared component:
* World edges
* Russia, Samara region locals
'''

README = README(MODULE)
diroot // README
README.sync()

mk = MODULE.mk

simpl = 'TM_WORLD_BORDERS_SIMPL-0.3'

loader = Section('loader', 0)

mk.all.dropall() //\
    (S(f'.PHONY: all\nall: {simpl}.readme \\') //
     f'{simpl}.shp Regions.shp location.json') //\
    (S(f'location.json: ','',0) //
     " ".join(f"{r}.shp" for r in REGIONS) //
     loader)

mk.mid // (S(f'%.shp: tmp/%.zip') //
           'unzip $< && touch $@ && ogrinfo $@'//
           f'mv Readme.txt {simpl}.readme'
           ) //\
    (S(f'tmp/{simpl}.zip:') //
     f'$(WGET) -O $@ https://thematicmapping.org/downloads/{simpl}.zip'
     ) //\
    (S('tmp/Regions.zip:') //
     '$(WGET) -O $@ http://gisgeo.org/assets/files/Regions.zip'
     )

w = '$(PY) $(MODULE).py'
loader // f'{w} ['
idx = 1
for r in REGIONS:
    mk.mid //\
        (S(f'{r}.shp: Regions.shp Makefile') //
            f"ogr2ogr -where \"NAME='{REGIONS[r]}'\" -lco ENCODING=UTF-8 $@ $<")
    #  f"ogr2ogr -f SQLite {self}.sqlite3 -sql \"select name from Regions where name='{self.regions[r]}'\" $<")
    a = f'{r}.shp'
    b = f'"{REGIONS[r]}"'
    loader // f'{w} {a:<13} {b:<22} {idx}'
    idx += 1
loader // f'{w} ]'

mk.sync()


py = MODULE.py

py.mid // """

import sys, re, shapefile

json = 'location.json'

if sys.argv[1] == '[':
    open(json, 'w').write("[")
    sys.exit(0)
if sys.argv[1] == ']':
    with open(json, 'a') as a:
        a.seek(0,2)
        a.truncate(a.tell()-1)
        a.write("\\n]\\n")
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
        j.write(\"\"\"
{
	"model": "app.location",
	"pk": %s,
	"fields": {
		"name":  "%s",
        "shape": "SRID=4326;POLYGON ((%s))"
	}
},\"\"\" % (sys.argv[3], sys.argv[2], dat))

"""

py.sync()

(MODULE.giti // '/*.dbf').sync()
(MODULE.apt // 'gdal-bin').sync()
(MODULE.reqs // 'pyshp').sync()
(MODULE.tmp.giti // '*.zip').sync()

## @}
