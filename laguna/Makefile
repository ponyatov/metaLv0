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
SRC += manage.py
SRC += proj/context.py
SRC += proj/settings.py
SRC += proj/urls.py
SRC += app/admin.py
SRC += app/apps.py
SRC += app/forms.py
SRC += app/models.py
SRC += app/views.py
# / <section:src>
# \ <section:all>
.PHONY: all
all: $(PY) manage.py
	$^
# / <section:all>
# \ <section:doc>
.PHONY: doc
doc:
# / <section:doc>
# \ <section:runserver>
.PHONY: runserver
runserver: $(PY) manage.py
	$^ $@ 127.0.0.1:26746
# / <section:runserver>
# \ <section:check>
.PHONY: check
check: $(PY) manage.py
	$^ $@
# / <section:check>
# \ <section:makemigrations>
.PHONY: makemigrations
makemigrations: $(PY) manage.py
	$^ $@ app
# / <section:makemigrations>
# \ <section:migrate>
.PHONY: migrate
migrate: $(PY) manage.py
	$(MAKE) makemigrations
	$^ $@
# / <section:migrate>
# \ <section:createsuperuser>
.PHONY: createsuperuser
createsuperuser: $(PY) manage.py
	$^ $@ \
		--username dponyatov \
		--email dponyatov@gmail.com
# / <section:createsuperuser>
# \ <section:dumpdata>
.PHONY: dumpdata
dumpdata: $(PY) manage.py
	$^ dumpdata --indent 2 -o $@
# / <section:dumpdata>
# \ <section:loaddata>
.PHONY: loaddata
loaddata: $(PY) manage.py
	$^ loaddata user.json location.json
# / <section:loaddata>
# / <section:mid>
# \ <section:bot>
# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) doc
	$(MAKE) $(PIP)
	$(PIP)  install    -r requirements.pip
	ln -fs  ../../world/location.json fixture/location.json
	$(MAKE) js
	$(MAKE) migrate
	$(MAKE) createsuperuser
	$(MAKE) loaddata
# / <section:install>
# \ <section:update>
.PHONY: update
update:
	$(MAKE) $(OS)_update
	$(PIP)  install -U    pip
	$(PIP)  install -U -r requirements.pip
# \ <section:js/install>
.PHONY: js
js: \
	static/jquery.js \
	static/bootstrap.css static/bootstrap.js \
	static/leaflet.js
# \ <section:js/jquery>
JQUERY_VER = 3.5.0
static/jquery.js:
	$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js
# / <section:js/jquery>
# \ <section:js/bootstrap>
BOOTSTRAP_VER = 3.4.1
BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css
static/bootstrap.js:
	$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js
# / <section:js/bootstrap>
# \ <section:js/leaflet>
LEAFLET_VER = 1.7.1
LEAFLET_ZIP = http://cdn.leafletjs.com/leaflet/v$(LEAFLET_VER)/leaflet.zip
static/leaflet.js: $(TMP)/leaflet.zip
	unzip -d static $< leaflet.css leaflet.js* images/* && touch $@
$(TMP)/leaflet.zip:
	$(WGET) -O $@ $(LEAFLET_ZIP)
# / <section:js/leaflet>
# / <section:js/install>
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
	-sudo apt update
	-sudo apt install -u `cat apt.txt`
# / <section:linux/install>
# \ <section:merge>
MERGE  = Makefile apt.txt .gitignore .vscode
MERGE += doc src tmp README.md
MERGE += requirements.pip $(MODULE).py test_$(MODULE).py
MERGE += static templates
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
