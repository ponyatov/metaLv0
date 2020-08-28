
# \ <section:top>
# powered by metaL: https://repl.it/@metaLmasters/metaL#README.md 
# @file# @file

# \ <section:vars>
CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)
# / <section:vars>

# \ <section:git>
NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)
# / <section:git>
# / <section:top>
# \ <section:mid>

# \ <section:tools>
WGET    = wget -c --no-check-certificate
OBJDUMP = LANG=C objdump
CLANG   = LANG=C clang
LLC     = LANG=C llc
CC      = $(CLANG)
# / <section:tools>

# \ <section:src>
SRC += $(MODULE).objdump
SRC += empty.ll empty.s empty.objdump empty.c
SRC += hello.ll hello.s hello.objdump hello.c
SRC += ll.ll ll.s ll.objdump
# / <section:src>

# \ <section:obj>
OBJ += empty.o
OBJ += hello.o
OBJ += ll.o
WASM += ll.wasm
# / <section:obj>

# \ <section:all>
.PHONY: all
all: $(MODULE)
	./$^
$(MODULE): $(OBJ) $(SRC) $(WASM)
	$(CC) -o $@ $(OBJ)
# / <section:all>

# \ <section:rules>
%.ll: %.c
	$(CLANG) -S -emit-llvm -o $@ $<
%.s: %.ll
	$(LLC) -o $@ $<
%.o: %.s
	$(CLANG) -c -o $@ $<
%.wasm: %.ll
	$(LLC) -march=wasm32 -filetype=obj -o $@ $<
	wasm-objdump -dx $@ > $@.objdump
%.objdump: %.o
	$(OBJDUMP) -dx $< > $@
# / <section:rules>
$(MODULE).objdump: $(MODULE)
	$(OBJDUMP) -dx $< > $@
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
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`

# / <section:bot>