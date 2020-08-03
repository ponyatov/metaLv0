
// Multiboot Specification version 0.6.96
// https://www.gnu.org/software/grub/manual/multiboot/multiboot.html
// https://github.com/dom96/nimkernel/blob/master/boot.s

#include "demos.h"

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

