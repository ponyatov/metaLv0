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
TCC      = tcc
CC       = $(TCC)
CXX      = g++
AS       = $(CC)
LD       = $(CC)
OBJDUMP  = objdump
SIZE     = size
RAGEL    = ragel
# / <section:tools>
# \ <section:flags>
OPT      = -O0 -g2
CFLAGS   = $(OPT) -I$(SRC) -I$(TMP)
# / <section:flags>
# / <section:top>
# \ <section:mid>
# \ <section:obj>
OBJ     += $(TMP)/NMEA.o
OBJ     += $(TMP)/ragel.o
# / <section:obj>
.PHONY: all
all:
	$(MAKE) test
.PHONY: test
test: $(BIN)/$(MODULE) sample.nmea
	$^ | head -n22
.PHONY: repl
repl:
	$(MAKE) test
	$(MAKE) $@
# \ <section:doc>
.PHONY: doc
doc:

# / <section:doc>
# \ <section:rules>
$(BIN)/$(MODULE): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^
$(TMP)/%.o: $(SRC)/%.c $(SRC)/$(MODULE).h $(SRC)/%.h
	$(CC) $(CFLAGS) -o $@ -c $<
$(TMP)/%.o: $(SRC)/%.c $(SRC)/$(MODULE).h
	$(CC) $(CFLAGS) -o $@ -c $<
$(TMP)/%.o: $(TMP)/%.c $(SRC)/$(MODULE).h $(TMP)/%.h
	$(CC) $(CFLAGS) -o $@ -c $<
$(TMP)/%.o: $(TMP)/%.c $(SRC)/$(MODULE).h
	$(CC) $(CFLAGS) -o $@ -c $<
$(SRC)/ragel.c: $(SRC)/$(MODULE).ragel
	$(RAGEL) -G2 -o $@ $<
# / <section:rules>
.PHONY: ragel
ragel: $(SRC)/ragel.c
# / <section:mid>
# \ <section:bot>
# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
	$(MAKE) doc
# / <section:install>
# \ <section:update>
.PHONY: update
update:
	$(MAKE) $(OS)_update
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
