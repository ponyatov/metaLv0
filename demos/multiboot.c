
// Multiboot Specification version 0.6.96
// https://www.gnu.org/software/grub/manual/multiboot/multiboot.html
// https://github.com/dom96/nimkernel/blob/master/boot.s

#include "demos.h"

struct MULTIBOOT multiboot __attribute__((section(".multiboot")))
    = {MULTIBOOT_HEADER_MAGIC,MULTIBOOT_FLAGS,MULTIBOOT_CHECKSUM};

void init() { main(); for(;;); }

