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
# / <section:python tools>
# / <section:head>
# \ <section:webook>

.PHONY: all
all: $(PY) $(MODULE).py
	$^

PHONY: repl
repl: $(PY) $(MODULE).py metaL.py
	$(PY) -i $(MODULE).py
	$(MAKE) $@
# / <section:webook>
# \ <section:tail>

# \ <section:install>

.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) $(PIP)
	$(PIP) install    -r requirements.txt
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
# / <section:tail>
