# \ <section:head>

CWD     = $(CURDIR)
MODULE  = $(notdir $(CWD))
OS     ?= $(shell uname -s)

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)

# / <section:head>

# \ <section:demos>

# \ <section:backend tools: TCC magic>

OPT     = -m32 -fno-pic -mtune=i386 -O0
CC      = gcc $(OPT)
AS      = gcc $(OPT)
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
	$(CC) -o $@ -c $< && $(OBJDUMP) -xdas $@ > $@.dump
%.o: %.c $(H) Makefile
	$(CC) -o $@ -c $< && $(OBJDUMP) -xdas $@ > $@.dump

# / <section:macro rules>



# / <section:demos>


# \ <section:tail>


# / <section:tail>

