## @file
## @brief @ref unikernel OS model

from metaL import *

## @defgroup demos demos
## @brief @ref unikernel OS model
## @{

MODULE = Module('demos')
vm['MODULE'] = MODULE

TITLE = Title('`unikernel` OS model in metaL/py')
vm['TITLE'] = TITLE

ABOUT = String('''
It's an operating system model treated as a demo of writing a language-powered
OS in Python, which was mentioned in https://t.me/osdev channel a few weeks ago.
It is not something more than just a fun toy, not targets for any practical use
or Linux killer.

On the other side, I don't see a lot of projects on implementing hobby OS based
on some language interpreter, compiler embedded into the OS kernel, or
standalone interactive development system, as it was popular in the 80th.

So, in this demo, I'm going to mix a bytecode interpreter, a few bare-metal
drivers written in C and assembly, and the method of concept programming in
Python. Also, it should run in a *guest OS* mode as generic application over
mainstream OS such as Linux.

* hw: i386/QEMU
* powered by `metaL`''')
vm['ABOUT'] = ABOUT

## `~/metaL/$MODULE` target directory for code generation
diroot = Dir(MODULE)
vm['dir'] = diroot

## file masks will be ignored by `git` version manager
gitignore = gitIgnore('.gitignore')
vm['gitignore'] = gitignore
diroot // gitignore
gitignore // '*.dump\n*.kernel'
gitignore.sync()

## `Makefile` for target project build/run
mk = Makefile()
vm['mk'] = mk
diroot // mk
mksection = Section(MODULE)
mk // mksection
mktools = Section('backend tools: TCC magic')
mksection // mktools
mktools // 'OPT     = -m32 -fno-pic -mtune=i386 -O0'
mktools // 'CC      = gcc $(OPT)'
mktools // 'AS      = gcc $(OPT)'
mktools // 'LD      = ld'
mktools // 'OBJDUMP = LANG=C objdump'
mksection // 'H   += multiboot.h $(MODULE).h'
mksection // 'OBJ += multiboot.o $(MODULE).o'
mksection // '\n.PHONY: all\nall: $(MODULE).kernel'
mksection // '\tqemu-system-i386 -m 2M -kernel $<'
objdump = '$(OBJDUMP) -xdas $@ > $@.dump'
mksection // '\n$(MODULE).kernel: $(OBJ) multiboot.ld Makefile'
mksection // ('\t$(LD) -nostdlib -T multiboot.ld -o $@ $(OBJ) && ' + objdump + '\n')
mkrules = Section('macro rules')
mksection // mkrules
compiler = ('%%.o: %%.%s $(H) Makefile\n\t$(CC) -o $@ -c $< && ' + objdump)
mkrules // (compiler % 's')
mkrules // (compiler % 'c')
mk.sync()

## `README.md`
readme = File('README.md')
diroot // readme
readme // ('#  `%s`' % MODULE.val)
readme // ('## %s' % TITLE.val)
readme // ''
readme // ('(c) %s <<%s>> %s %s' %
           (AUTHOR.val, EMAIL.val, YEAR.val, LICENSE.val))
readme // ''
readme // ('github: %s/%s/blob/master/%s.py' %
           (GITHUB.val, vm.val, MODULE.val))
readme // ABOUT
readme.sync()

ldfile = File('multiboot.ld')
diroot // ldfile
ldfile // '''
OUTPUT_FORMAT("elf32-i386")
OUTPUT_ARCH(i386)

SECTIONS
{
    .text : { *(.multiboot) *(.text*)    }
    .data : { *(.data)                   }
    .bss  : { *(.bss)                    }
    /DISCARD/ : { *(.comment*) *(.note*) *(.eh_frame) *(.got) }
}
'''
ldfile.sync()

header = cFile('%s.h'%MODULE.val)
diroot // header
header // '''
#ifndef _H_DEMOS
#define _H_DEMOS

#include <stdint.h>
#include "multiboot.h"

extern void init(void);
extern void main(void);

// extern uint8_t *VGA;// = (uint8_t*) 0xB8000;

struct _VGA {
    uint8_t ch;
    uint8_t attr;
} __attribute__((packed));

extern struct _VGA *VGA;
extern uint16_t cursor;

#endif // _H_DEMOS
'''
header.sync()

bootheader = '''
// Multiboot Specification version 0.6.96
// https://www.gnu.org/software/grub/manual/multiboot/multiboot.html
// https://github.com/dom96/nimkernel/blob/master/boot.s
'''

incheader = ('#include "%s.h"' % MODULE.val)

booth = cFile('multiboot.h')
diroot // booth
booth // bootheader
booth // incheader
booth // '''
#ifndef _H_MULTIBOOT
#define _H_MULTIBOOT

#define MULTIBOOT_PAGE_ALIGN       (1<<0) // align to page boundaries
#define MULTIBOOT_MEMORY_INFO      (1<<1) // provide memory map

#define MULTIBOOT_HEADER_MAGIC     0x1BADB002
#define MULTIBOOT_BOOTLOADER_MAGIC 0x2BADB002
#define MULTIBOOT_FLAGS            (MULTIBOOT_PAGE_ALIGN)//|MULTIBOOT_MEMORY_INFO)
#define MULTIBOOT_CHECKSUM         (-(MULTIBOOT_HEADER_MAGIC + MULTIBOOT_FLAGS))

struct MULTIBOOT {
    uint32_t magic;
    uint32_t flags;
    uint32_t checksum;
} __attribute__((packed));

#endif // _H_MULTIBOOT
'''
booth.sync()

bootc = cFile('multiboot.c')
diroot // bootc
bootc // bootheader
bootc // incheader
bootc // '''
struct MULTIBOOT multiboot __attribute__((section(".multiboot")))
    = {MULTIBOOT_HEADER_MAGIC,MULTIBOOT_FLAGS,MULTIBOOT_CHECKSUM};

void init() { main(); for(;;); }
'''
bootc.sync()

kernel = cFile('%s.c'%MODULE.val)
diroot // kernel
kernel // incheader
kernel // '''

struct _VGA *VGA = (struct _VGA *) 0xB8000;

uint16_t cursor = 0;

void main(void) {
    VGA[cursor  ].ch   = 'H';
    VGA[cursor++].attr = 0x1F;
    VGA[cursor  ].ch   = 'E';
    VGA[cursor++].attr = 0x1F;
    VGA[cursor  ].ch   = 'L';
    VGA[cursor++].attr = 0x1F;
    VGA[cursor  ].ch   = 'L';
    VGA[cursor++].attr = 0x1F;
    VGA[cursor  ].ch   = 'O';
    VGA[cursor++].attr = 0x1F;
}
'''
kernel.sync()

print(vm)

## @}
