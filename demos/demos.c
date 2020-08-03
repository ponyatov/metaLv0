#include "demos.h"


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

