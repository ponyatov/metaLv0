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
LIB      = $(CWD)/lib
TMP      = $(CWD)/tmp
SRC      = $(CWD)/src
GZ       = $(HOME)/gz
# / <section:dirs>
# \ <section:tools>
WGET     = wget -c --no-check-certificate
CORES    = $(shell grep proc /proc/cpuinfo|wc -l)
XPATH    = PATH=$(BIN):$(PATH)
XMAKE    = $(XPATH) $(MAKE) -j$(CORES)
IEX      = iex
MIX      = mix
ELIXIR   = elixir
ELIXIRC  = elixirc
# / <section:tools>
# / <section:top>
# \ <section:mid>
.PHONY: all
all:
	$(MAKE) test
.PHONY: test
test:
	$^
	$(MIX) format
	$(MIX) test
.PHONY: repl
repl:
	$(MAKE) test
	# \ <section:repl>
	$(IEX)  -S $(MIX)
	# / <section:repl>
	$(MAKE) $@
# \ <section:doc>
.PHONY: doc
doc:

# / <section:doc>
# \ <section:rules>
static/%: $(HOME)/icons/%
	cp $< $@
static/hedge64x64.png: $(HOME)/icons/logo64x64.png
	cp $< $@
static/logo.png: $(HOME)/icons/planning.png
	cp $< $@
# / <section:rules>
STATIC += static/logo.png static/chart.png static/clock.png
STATIC += static/hedgehog.png static/hedge64x64.png
STATIC += static/planning.png static/android_plan.png static/Rubik_64x64.png
.PHONY: static
static: $(STATIC)
# / <section:mid>
# \ <section:bot>
# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) doc
	$(MAKE) static
	$(MIX)  deps.get
	$(MIX)  compile
# / <section:install>
# \ <section:update>
.PHONY: update
update:
	$(MAKE) $(OS)_update
	$(MIX)  deps.get
	$(MIX)  compile
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
MERGE += lib .formatter.exs mix.exs
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
