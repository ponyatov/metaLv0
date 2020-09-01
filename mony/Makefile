
# \ <section:top>
#  powered by metaL: https://repl.it/@metaLmasters/metaL#README.md
## @file

# \ <section:vars>
MODULE   = $(notdir $(CURDIR))
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
# / <section:tools>

# \ <section:py/tools>
PIP = $(CWD)/bin/pip3
PY  = $(CWD)/bin/python3
PYT = $(CWD)/bin/pytest
PEP = $(CWD)/bin/autopep8 --ignore=E26,E302,E401,E402
# / <section:py/tools>
# / <section:top>
# \ <section:mid>

# \ <section:tools>
WGET    = wget -c --no-check-certificate
# / <section:tools>

# \ <section:src>
SRC += $(MODULE).py
SRC += manage.py
SRC += app/settings.py
SRC += proj/urls.py
SRC += app/apps.py
SRC += manage.py
SRC += app/admin.py
SRC += app/settings.py
SRC += proj/urls.py
# / <section:src>

# \ <section:obj>
# / <section:obj>

# \ <section:all>
.PHONY: all
all: $(PY) manage.py
	$^
# / <section:all>

# \ <section:rules>
# / <section:rules>

# \ <section:mony>

# \ <section:repl>
# / <section:repl>
# / <section:mony>

# \ <section:runserver>
.PHONY: runserver
runserver: $(PY) manage.py
	$^ $@
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

# \ <section:shell>
.PHONY: shell
shell: $(PY) manage.py
	$^ $@
# / <section:shell>

# \ <section:startproject>
.PHONY: startproject
startproject: bin/django-admin
	$< startproject monyz
# / <section:startproject>
# / <section:mid>
# \ <section:bot>

# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) $(PIP)
	$(PIP) install    -r requirements.txt
	$(MAKE) js
	$(MAKE) migrate
	$(MAKE) createsuperuser
# / <section:install>

# \ <section:update>
.PHONY: update
update:
	$(MAKE) $(OS)_update
	$(PIP) install -U    pip
	$(PIP) install -U -r requirements.txt

# / <section:update>

# \ <section:linux/install>
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

# / <section:linux/install>

# \ <section:merge>
MERGE  = Makefile apt.txt .gitignore
MERGE += README.md
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
# / <section:bot>