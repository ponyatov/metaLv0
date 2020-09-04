
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
TCC      = tcc
CC       = $(TCC)
CXX      = g++
AS       = $(CC)
LD       = $(CC)
OBJDUMP  = objdump
SIZE     = size
# / <section:tools>

# \ <section:flags>
OPT      = -O0 -g2 
CFLAGS   = $(OPT) -I.
# / <section:flags>
# / <section:top>
# \ <section:mid>

# \ <section:src>
H += bcx.h
C += bcx.c
BCX_C += bcx.c
H += asm.hpp
H += parser.h
ASM_C += asm.cpp
ASM_C += lexer
ASM_C += parser.c
# / <section:src>

# \ <section:obj>
OBJ += bcx
OBJ += bcx.bcx
# / <section:obj>

# \ <section:all>
.PHONY: all
all: bcx bcx.bcx
	./$^
# / <section:all>

# \ <section:rules>
%.bcx: asm %.4th
	./$^
%.c: %.lex
	flex -o $@ $<
%.c: %.yacc
	bison -o $@ $<
asm: $(ASM_C) $(H)
	$(CXX) $(CFLAGS) -o $@ $(ASM_C)
bcx: $(BCX_C) $(H)
	$(CC) $(CFLAGS) -o $@ $(BCX_C)
# / <section:rules>
# / <section:mid>
# \ <section:bot>

# \ <section:install>
.PHONY: install
install:
	$(MAKE) $(OS)_install
# / <section:install>

# \ <section:update>
.PHONY: update
update:
	$(MAKE) $(OS)_update
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
# / <section:bot>