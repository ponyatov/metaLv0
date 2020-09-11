
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file
# \ <section:top>
# \ <section:vars>
MODULE   = metaL
OS      ?= $(shell uname -s)
# / <section:vars>
# \ <section:version>
NOW      = $(shell date +%d%m%y)
REL      = $(shell git rev-parse --short=4 HEAD)
# / <section:version>
# \ <section:dirs>
CWD      = $(CURDIR)
TMP      = $(CWD)/tmp
SOURCE   = $(TMP)/src
# / <section:dirs>
# \ <section:tools>
WGET     = wget -c --no-check-certificate
CORES    = $(shell grep proc /proc/cpuinfo|wc -l)
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
all: repl
.PHONY: repl
repl: $(PYT) $(PY) metaL.py
	$(PYT) test_metaL.py
	$(PY) -i metaL.py
	$(MAKE) $@
# / <section:all>
# / <section:mid>
# \ <section:bot>
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
# \ <section:py/install>
$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
$(PYT):
	$(PIP) install -U pytest
# / <section:py/install>
# \ <section:linux/install>
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# / <section:linux/install>
# \ <section:merge>
MERGE  = Makefile apt.txt .gitignore
MERGE += README.md
MERGE += $(MODULE).py
# / <section:merge>
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
# / <section:bot>