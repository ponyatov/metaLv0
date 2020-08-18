CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest
PEP = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402

WGET  = wget -c --no-check-certificate
CORES = $(shell grep proc /proc/cpuinfo|wc -l)
XMAKE = $(MAKE) -j$(CORES)



.PHONY: all
all: repl

.PHONY: repl
repl: $(PY) $(MODULE).py $(MODULE).ini config.py
	-$(MAKE) doxy
	$(MAKE) test
	$(PY) -i $(MODULE).py $(MODULE).ini
	$(MAKE) $@

.PHONY: test
test: $(PYT) test_$(MODULE).py $(MODULE).py $(MODULE).ini config.py
	$(PYT) test_$(MODULE).py

%/repl: %.py $(PY)
	-$(MAKE) doxy
	$(MAKE) test
	$(PY) -i $<
	$(MAKE) $@



SRC = $(shell find $(CWD) -maxdepth 1 -type f -regex .+.py$$)

.PHONY: pep
pep:
	echo $(SRC) | xargs -n1 -P0 $(PEP) -i

.PHONY: doxy
doxy: doc/tutorial.svg doc/taxonomy.svg doc/hosttarget.svg
#	doxygen -g doxy.gen
	doxygen doxy.gen 1>/dev/null
doc/%.svg: doc/%.dot
	dot -Tsvg -o $@ $<

.PHONY: pdf
pdf: doc/pdf/InsideSmalltalk_I.pdf doc/pdf/InsideSmalltalk_II.pdf \
		doc/pdf/ALittleSmalltalk.pdf doc/pdf/Bluebook.pdf
doc/pdf/InsideSmalltalk_I.pdf:
	$(WGET) -O $@ http://sdmeta.gforge.inria.fr/FreeBooks/InsideST/InsideSmalltalk.pdf
doc/pdf/InsideSmalltalk_II.pdf:
	$(WGET) -O $@ http://sdmeta.gforge.inria.fr/FreeBooks/InsideST/InsideSmalltalkII.pdf
doc/pdf/ALittleSmalltalk.pdf:
	$(WGET) -O $@ http://sdmeta.gforge.inria.fr/FreeBooks/LittleSmalltalk/ALittleSmalltalk.pdf
doc/pdf/Bluebook.pdf:
	$(WGET) -O $@ http://sdmeta.gforge.inria.fr/FreeBooks/BlueBook/Bluebook.pdf



.PHONY: install update

install: $(PIP)
	-$(MAKE) $(OS)_install
	$(PIP)   install    -r requirements.txt
update: $(PIP)
	-$(MAKE) $(OS)_update
	$(PIP)   install -U    pip
	$(PIP)   install -U -r requirements.txt
	$(MAKE)  requirements.txt

$(PIP) $(PY):
	python3 -m venv .
	$(PIP) install -U pip pylint autopep8
	$(MAKE) requirements.txt
$(PYT):
	$(PIP) install -U pytest
	$(MAKE) requirements.txt

.PHONY: requirements.txt
requirements.txt: $(PIP)
	$< freeze | egrep "py(lint|test)|autopep8|ply|xxhash" > $@


.PHONY: Linux_install Linux_update

Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`



.PHONY: master shadow release

MERGE  = Makefile README.md .vscode/tasks.json apt.txt doxy.gen
MERGE += $(MODULE).py test_$(MODULE).py $(MODULE).ini static
MERGE += requirements.txt pyproject.toml .replit doc
MERGE += $(MODULE) metacircular.py
MERGE += Smalltalk.py
MERGE += dja dja.py
MERGE += demos demos.py
MERGE += webook webook.py
MERGE += rdbms rdbms.py

master:
	rm -rf docs
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
	$(MAKE) doxy

shadow:
	rm -rf docs
	git checkout docs
	git checkout $@
	git pull -v
	$(MAKE) doxy

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
