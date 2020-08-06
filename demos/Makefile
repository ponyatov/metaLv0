# \ <section:head>

CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)


# / <section:head>

# \ <section:demos>

# \ <section:backend tools: TCC magic>

CFLAGS  = -m32 -O0
CC      = tcc
AS      = tcc
LD      = ld
OBJDUMP = LANG=C objdump

# / <section:backend tools: TCC magic>


H   += multiboot.h $(MODULE).h
OBJ += multiboot.o $(MODULE).o

.PHONY: all
all: $(MODULE).kernel
	qemu-system-i386 -m 2M -kernel $<

$(MODULE).kernel: $(OBJ) multiboot.ld Makefile
	$(LD) -nostdlib -T multiboot.ld -o $@ $(OBJ) && $(OBJDUMP) -xdas $@ > $@.dump

# \ <section:macro rules>

%.o: %.s $(H) Makefile
	$(CC) $(CFLAGS) -o $@ -c $< && $(OBJDUMP) -xdas $@ > $@.dump
%.o: %.c $(H) Makefile
	$(CC) $(CFLAGS) -o $@ -c $< && $(OBJDUMP) -xdas $@ > $@.dump

# / <section:macro rules>



# / <section:demos>


# \ <section:tail>

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


WGET  = wget -c --no-check-certificate

.PHONY: Linux_install Linux_update

Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`


# / <section:tail>

