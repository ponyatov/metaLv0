## @file
## @brief `drtos`: distributed/embedded [RT]OS patterns

from metaL import *

## @defgroup os OS
## @ingroup samples
## @brief `drtos`: distributed/embedded [RT]OS patterns
## @{

class osModule(anyModule):

    def __init__(self, V=None):
        super().__init__(V)
        self.init_firmware()

    def init_firmware(self):
        self.diroot['firmware'] = self.diroot.firmware = Dir('firmware')
        self.diroot // self.diroot.firmware
        self.diroot.firmware.giti = File('.gitignore') // '*'
        self.diroot.firmware // self.diroot.firmware.giti
        self.diroot.firmware.giti.sync()

    def init_apt(self):
        super().init_apt()
        self.apt //\
            'binutils tcc' //\
            'build-essential binutils gcc flex bison bc' //\
            'syslinux qemu-system-i386'
        self.apt.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f11.cmd.val = 'make qemu'
        self.f12.cmd.val = 'make build'
        self.vscode.settings.sync()

## @}
