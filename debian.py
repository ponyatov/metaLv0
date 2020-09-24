
from metaL import *

DEBIAN_VER = "10.5.0"
DEBIAN_ARCH = "i386"
DEBIAN_LIVE_ISO = f'debian-live-{DEBIAN_VER}-{DEBIAN_ARCH}-standard+nonfree.iso'
DEBIAN_URL = f"https://cdimage.debian.org/images/unofficial/non-free/images-including-firmware/{DEBIAN_VER}-live+nonfree/{DEBIAN_ARCH}/iso-hybrid/{DEBIAN_LIVE_ISO}"

VIRTUALBOX_VER = '6.1'

class debModule(anyModule):

    def init_mk(self):
        super().init_mk()
        #
        self.mk.mid //\
            S(f'all: vbox') //\
            (S(f'{DEBIAN_LIVE_ISO}:') // f'$(WGET) -O $@ {DEBIAN_URL}')
        #
        self.init_vbox()
        #
        self.mk.sync()

    def init_vbox(self):
        # https://www.andreafortuna.org/2019/10/24/how-to-create-a-virtualbox-vm-from-command-line/
        # https://www.virtualbox.org/manual/ch08.html
        self.mk.mid // (S(f'.PHONY: vbox\nvbox: {DEBIAN_LIVE_ISO}') //
                        f'-VBoxManage createvm --name {self} --ostype Debian --register --basefolder $(CWD)/$@' //
                        f'-VBoxManage modifyvm {self} --memory 2048 --vram 64 --ioapic on' //
                        f'-VBoxManage createhd --filename $(CWD)/$@/{self}.vdi --size 16 --format VDI' //
                        f'-VBoxManage storagectl {self} --name "SATA" --add sata --controller IntelAhci' //
                        f'-VBoxManage storageattach {self} --storagectl "SATA" --port 0 --device 0 --type hdd --medium $(CWD)/$@/{self}.vdi' //
                        f'-VBoxManage storagectl {self} --name "IDE" --add ide --controller PIIX3' //
                        f'-VBoxManage storageattach {self} --storagectl "IDE" --port 1 --device 0 --type dvddrive --medium $<' //
                        f'-VBoxManage modifyvm {self} --boot1 dvd --boot2 disk --boot3 none --boot4 none' //
                        f'-VBoxManage modifyvm {self} --audio none' //
                        f'-VBoxManage modifyvm {self} --nic1 nat' //
                        f'-VBoxManage modifyvm {self} --usbohci on' //
                        ''
                        )
        self.vbox = Dir('vbox')
        self.diroot // self.vbox
        self.vbox.sync()
        self.vbox.giti = File('.gitignore')
        self.vbox // self.vbox.giti
        (self.vbox.giti // '*').sync()

    def init_giti(self):
        super().init_giti()
        self.giti.mid // f'/{DEBIAN_LIVE_ISO}'
        self.giti.sync()

    def init_apt(self):
        super().init_apt()
        (self.apt // 'syslinux' // f'virtualbox-{VIRTUALBOX_VER}').sync()


MODULE = debModule()

MODULE['TITLE'] = TITLE = Title(
    f'live USB install: Debian GNu/Linux {DEBIAN_VER} {DEBIAN_ARCH}')

MODULE['ABOUT'] = ABOUT = f'''
`metaL` usage so easy as it can be used to do even such light and temporary tasks:
in place of writing Shell scripts or `Makefile` manually we can generate the
generic project with the `Makefile` and provide a list of required programs for
the host system in a few lines of Python code.

sample `anyModule`-based project just to download & install Debian {DEBIAN_ARCH} `.iso`
'''

README = README(MODULE)
MODULE['dir'] // README
README.sync()
