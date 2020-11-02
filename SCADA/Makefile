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
ERL      = erl
ERLC     = erlc
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
doc: doc/Programming_Erlang_ru.pdf doc/Learn_You_Some_Erlang_For_Great_Good_ru.pdf doc/n2o.pdf

doc/Programming_Erlang_ru.pdf:
	$(WGET) -O $@ https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/fullbook.pdf
doc/Learn_You_Some_Erlang_For_Great_Good_ru.pdf:
	$(WGET) -O $@ https://github.com/mpyrozhok/learnyousomeerlang_ru/raw/master/pdf/learnyousomeerlang_ru.pdf
doc/n2o.pdf:
	$(WGET) -O $@ https://n2o.dev/books/n2o.pdf
# / <section:doc>
# / <section:mid>
# \ <section:bot>
# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) doc
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
