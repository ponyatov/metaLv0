
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
# \ <section:vars>
# \ <section:module>
MODULE   = $(notdir $(CURDIR))
# / <section:module>
OS      ?= $(shell uname -s)
# / <section:vars>
# \ <section:version>
NOW      = $(shell date +%d%m%y)
REL      = $(shell git rev-parse --short=4 HEAD)
# / <section:version>
# \ <section:dirs>
CWD      = $(CURDIR)
BIN      = $(CWD)/bin
TMP      = $(CWD)/tmp
SOURCE   = $(TMP)/src
# / <section:dirs>
# \ <section:tools>
WGET     = wget -c --no-check-certificate
CORES    = $(shell grep proc /proc/cpuinfo|wc -l)
XPATH    = PATH=$(BIN):$(PATH)
XMAKE    = $(XPATH) $(MAKE) -j$(CORES)
# / <section:tools>
# / <section:top>
# \ <section:mid>
all: vbox

debian-live-10.5.0-i386-standard+nonfree.iso:
	$(WGET) -O $@ https://cdimage.debian.org/images/unofficial/non-free/images-including-firmware/10.5.0-live+nonfree/i386/iso-hybrid/debian-live-10.5.0-i386-standard+nonfree.iso

.PHONY: vbox
vbox: debian-live-10.5.0-i386-standard+nonfree.iso
	-VBoxManage createvm --name debian --ostype Debian --register --basefolder $(CWD)/$@
	-VBoxManage modifyvm debian --memory 2048 --vram 64 --ioapic on
	-VBoxManage createhd --filename $(CWD)/$@/debian.vdi --size 16 --format VDI
	-VBoxManage storagectl debian --name "SATA" --add sata --controller IntelAhci
	-VBoxManage storageattach debian --storagectl "SATA" --port 0 --device 0 --type hdd --medium $(CWD)/$@/debian.vdi
	-VBoxManage storagectl debian --name "IDE" --add ide --controller PIIX3
	-VBoxManage storageattach debian --storagectl "IDE" --port 1 --device 0 --type dvddrive --medium $<
	-VBoxManage modifyvm debian --boot1 dvd --boot2 disk --boot3 none --boot4 none
	-VBoxManage modifyvm debian --audio none
	-VBoxManage modifyvm debian --nic1 nat
	-VBoxManage modifyvm debian --usbohci on
	

# / <section:mid>
# \ <section:bot>
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
# \ <section:linux/install>
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# / <section:linux/install>
# \ <section:merge>
MERGE  = Makefile apt.txt .gitignore .vscode
MERGE += README.md
# / <section:merge>
master:
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
shadow:
	git checkout $@
	git pull -v
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
# / <section:bot>