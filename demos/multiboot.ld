
OUTPUT_FORMAT("elf32-i386")
OUTPUT_ARCH(i386)

SECTIONS
{
    .text : { *(.multiboot) *(.text*)    }
    .data : { *(.data)                   }
    .bss  : { *(.bss)                    }
    /DISCARD/ : { *(.comment*) *(.note*) *(.eh_frame) *(.got) }
}

