
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
all: $(PY) $(MODULE).py
	$^

.PHONY: test
test: $(PYT) test_$(MODULE).py
	$^

.PHONY: $(MODULE)/repl
$(MODULE)/repl: $(PY) $(MODULE).py
	$(MAKE) test
	$(PY) -i $(MODULE).py
	$(MAKE) $@
# / <section:all>
# \ <section:doc>
.PHONY: doc
doc:
	$(MAKE) doc/SICP.pdf
doc/SICP.pdf:
	$(WGET) -O $@ https://newstar.rinet.ru/~goga/sicp/sicp.pdf
# / <section:doc>
# / <section:mid>
# \ <section:bot>
# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) doc
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