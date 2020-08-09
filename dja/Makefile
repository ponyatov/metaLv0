# \ <section:head>

CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

# \ <section:python tools>

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest
PEP = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402
DJA = $(CWD)/bin/django-admin

# / <section:python tools>

HOST = 127.0.0.1
PORT = 19999

# / <section:head>
# \ <section:dja>

.PHONY: all
all: $(PY) $(MODULE).py
	$^

PHONY: repl
repl: $(PY) $(MODULE).py metaL.py
	$(PY) -i $(MODULE).py
	$(MAKE) $@

.PHONY: runserver
runserver: $(PY) manage.py
$^ runserver $(HOST):$(PORT)

.PHONY: migrations
migrations: $(PY) manage.py
		$^ make$@

# / <section:dja>
# \ <section:tail>

# \ <section:install>

.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) $(PIP)
	$(PIP) install    -r requirements.txt
	$(MAKE) js

# / <section:install>
# \ <section:update>

.PHONY: update
update:
	$(MAKE) $(OS)_update
	$(PIP) install -U    pip
	$(PIP) install -U -r requirements.txt

# / <section:update>

WGET = wget -c --no-check-certificate

.PHONY: Linux_install Linux_update

Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

# \ <section:py/install>
$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
$(PYT):
	$(PIP) install -U pytest
# / <section:py/install>

# \ <section:js/install>
.PHONY: js
js: static/jquery.js static/bootstrap.css static/bootstrap.js

JQUERY_VER = 3.5.0
static/jquery.js:
	$(WGET) -O $@ https://code.jquery.com/jquery-$(JQUERY_VER).min.js

BOOTSTRAP_VER = 3.4.1
BOOTSTRAP_URL = https://stackpath.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.min.css
static/bootstrap.js:
	$(WGET) -O $@ $(BOOTSTRAP_URL)/js/bootstrap.min.js

# / <section:js/install>

# / <section:tail>
