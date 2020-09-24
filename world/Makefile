
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
# \ <section:vars>
# \ <section:module>
MODULE   = $(notdir $(CURDIR))
# / <section:module>
OS      ?= $(shell uname -s)
# / <section:vars>
# \ <section:version>
NOW      = $(shell date +%d%m%y)
REL      = $(shell git rev-parse --short=4 HEAD)
# / <section:version>
# \ <section:dirs>
CWD      = $(CURDIR)
BIN      = $(CWD)/bin
TMP      = $(CWD)/tmp
SRC      = $(CWD)/src
# / <section:dirs>
# \ <section:tools>
WGET     = wget -c --no-check-certificate
CORES    = $(shell grep proc /proc/cpuinfo|wc -l)
XPATH    = PATH=$(BIN):$(PATH)
XMAKE    = $(XPATH) $(MAKE) -j$(CORES)

PIP      = $(CWD)/bin/pip3
PY       = $(CWD)/bin/python3
PYT      = $(CWD)/bin/pytest
PEP      = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402

# / <section:tools>
# / <section:top>
# \ <section:mid>
# \ <section:src>
SRC += $(MODULE).py
# / <section:src>
# \ <section:all>
.PHONY: all
all: TM_WORLD_BORDERS_SIMPL-0.3.readme \
	TM_WORLD_BORDERS_SIMPL-0.3.shp Regions.shp location.json

location.json: Orenburg.shp Penza.shp Samara.shp Saratov.shp Ulianovsk.shp
	$(PY) $(MODULE).py [
	$(PY) $(MODULE).py Orenburg.shp  "Оренбургская область" 1
	$(PY) $(MODULE).py Penza.shp     "Пензенская область"   2
	$(PY) $(MODULE).py Samara.shp    "Самарская область"    3
	$(PY) $(MODULE).py Saratov.shp   "Саратовская область"  4
	$(PY) $(MODULE).py Ulianovsk.shp "Ульяновская область"  5
	$(PY) $(MODULE).py ]
# / <section:all>
%.shp: tmp/%.zip
	unzip $< && touch $@ && ogrinfo $@
	mv Readme.txt TM_WORLD_BORDERS_SIMPL-0.3.readme

tmp/TM_WORLD_BORDERS_SIMPL-0.3.zip:
	$(WGET) -O $@ https://thematicmapping.org/downloads/TM_WORLD_BORDERS_SIMPL-0.3.zip

tmp/Regions.zip:
	$(WGET) -O $@ http://gisgeo.org/assets/files/Regions.zip

Orenburg.shp: Regions.shp Makefile
	ogr2ogr -where "NAME='Оренбургская область'" -lco ENCODING=UTF-8 $@ $<

Penza.shp: Regions.shp Makefile
	ogr2ogr -where "NAME='Пензенская область'" -lco ENCODING=UTF-8 $@ $<

Samara.shp: Regions.shp Makefile
	ogr2ogr -where "NAME='Самарская область'" -lco ENCODING=UTF-8 $@ $<

Saratov.shp: Regions.shp Makefile
	ogr2ogr -where "NAME='Саратовская область'" -lco ENCODING=UTF-8 $@ $<

Ulianovsk.shp: Regions.shp Makefile
	ogr2ogr -where "NAME='Ульяновская область'" -lco ENCODING=UTF-8 $@ $<

# / <section:mid>
# \ <section:bot>
# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) $(PIP)
	$(PIP)  install    -r requirements.pip

# / <section:install>
# \ <section:update>
.PHONY: update
update:
	$(MAKE) $(OS)_update
	$(PIP)  install -U    pip
	$(PIP)  install -U -r requirements.pip

# \ <section:py/install>
$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
$(PYT):
	$(PIP) install -U pytest
# / <section:py/install>
# / <section:update>
# \ <section:linux/install>
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# / <section:linux/install>
# \ <section:merge>
MERGE  = Makefile apt.txt .gitignore .vscode
MERGE += README.md
MERGE += requirements.pip $(MODULE).py
# / <section:merge>
.PHONY: master shadow release zip

master:
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)

shadow:
	git checkout $@
	git pull -v

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow

zip:
	git archive --format zip \
		--output ~/tmp/$(MODULE)_src_$(NOW)_$(REL).zip \
		HEAD
	

# / <section:bot>