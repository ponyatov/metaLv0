
#ifndef _H_DEMOS
#define _H_DEMOS

#ifdef __TINYC__
#include <stddef.h>
#else
#include <stdint.h>
#endif

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

