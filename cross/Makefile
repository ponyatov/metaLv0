
#  powered by metaL: https://github.com/ponyatov/metaL/wiki/metaL-manifest
# \ <section:top>
# \ <section:vars>
# \ <section:module>
MODULE   = $(notdir $(CURDIR))
APP      = cross
HW       = qemu386
CPU      = i486dx
ARCH     = i386
TARGET   = i486-elf
# / <section:module>
OS      ?= $(shell uname -s)
# / <section:vars>
# \ <section:version>
NOW      = $(shell date +%d%m%y)
REL      = $(shell git rev-parse --short=4 HEAD)
# \ <section:cross>
GMP_VER      = 6.2.0
MPFR_VER     = 4.1.0
MPC_VER      = 1.2.0
BINUTILS_VER = 2.35.1
GDB_VER      = 9.2
GCC_VER      = 9.3.0
# / <section:cross>
# / <section:version>
# \ <section:dirs>
CWD      = $(CURDIR)
BIN      = $(CWD)/bin
TMP      = $(CWD)/tmp
SRC      = $(CWD)/src
GZ       = $(HOME)/gz
PFX      = $(CWD)/$(TARGET)
BIN      = $(PFX)/bin
LIB      = $(PFX)/lib
ROOT     = $(PFx)/root
FW       = $(CWD)/firmware
# / <section:dirs>
# \ <section:tools>
WGET     = wget -c --no-check-certificate
CORES    = $(shell grep proc /proc/cpuinfo|wc -l)
XPATH    = PATH=$(BIN):$(PATH)
XMAKE    = $(XPATH) $(MAKE) -j$(CORES)
# / <section:tools>
# / <section:top>
# \ <section:mid>
# \ <section:packages>
GMP      =      gmp-$(GMP_VER)
MPFR     =     mpfr-$(MPFR_VER)
MPC      =      mpc-$(MPC_VER)
BINUTILS = binutils-$(BINUTILS_VER)
GDB      =      gdb-$(GDB_VER)
GCC      =      gcc-$(GCC_VER)
# / <section:packages>
# \ <section:cfg>
CFG          = configure --prefix=$(PFX)
CFG_CCLIBS   = --disable-shared 
CFG_GMP      = $(CFG_CCLIBS)
CFG_MPFR     = $(CFG_CCLIBS)
CFG_MPC      = $(CFG_CCLIBS) --with-mpfr=$(PFX)
CFG_BINUTILS = \
	--target=$(TARGET) \
	--with-sysroot=$(ROOT) --with-native-system-header-dir=/include \
	--enable-lto --disable-multilib \
	--disable-nls

CFG_GDB      = $(CFG_BINUTILS)
CFG_GCC      = $(CFG_BINUTILS) \
	--enable-languages="c" \
	--with-gmp=$(PFX) --with-mpfr=$(PFX) --with-mpc=$(PFX)

CFG_GCC0     = $(CFG_GCC) --without-headers --with-newlib

# / <section:cfg>
# \ <section:cross>
.PHONY: cross
cross: cclibs gnu
# / <section:cross>
# \ <section:cclibs>
.PHONY: cclibs
cclibs: gmp mpfr mpc

.PHONY: gmp
gmp: $(LIB)/libgmp.a
$(LIB)/libgmp.a:
	$(MAKE) $(SRC)/$(GMP)/README
	rm -rf $(TMP)/$(GMP) ; mkdir -p $(TMP)/$(GMP) ; cd $(TMP)/$(GMP) ;\
	$(SRC)/$(GMP)/$(CFG) --help > $(TMP)/gmp.configure.help ;\
	$(XPATH) $(SRC)/$(GMP)/$(CFG) $(CFG_GMP) ;\
	$(XMAKE) &&\
	$(MAKE) install &&\
	touch $@ && rm -rf $(SRC)/$(GMP) $(TMP)/$(GMP)

.PHONY: mpfr
mpfr: $(LIB)/libmpfr.a
$(LIB)/libmpfr.a:
	$(MAKE) $(SRC)/$(MPFR)/README
	rm -rf $(TMP)/$(MPFR) ; mkdir -p $(TMP)/$(MPFR) ; cd $(TMP)/$(MPFR) ;\
	$(SRC)/$(MPFR)/$(CFG) --help > $(TMP)/mpfr.configure.help ;\
	$(XPATH) $(SRC)/$(MPFR)/$(CFG) $(CFG_MPFR) ;\
	$(XMAKE) &&\
	$(MAKE) install &&\
	touch $@ && rm -rf $(SRC)/$(MPFR) $(TMP)/$(MPFR)

.PHONY: mpc
mpc: $(LIB)/libmpc.a
$(LIB)/libmpc.a:
	$(MAKE) $(SRC)/$(MPC)/README
	rm -rf $(TMP)/$(MPC) ; mkdir -p $(TMP)/$(MPC) ; cd $(TMP)/$(MPC) ;\
	$(SRC)/$(MPC)/$(CFG) --help > $(TMP)/mpc.configure.help ;\
	$(XPATH) $(SRC)/$(MPC)/$(CFG) $(CFG_MPC) ;\
	$(XMAKE) &&\
	$(MAKE) install &&\
	touch $@ && rm -rf $(SRC)/$(MPC) $(TMP)/$(MPC)

# / <section:cclibs>
# \ <section:gnu>
.PHONY: gnu
gnu: binutils gdb gcc0

.PHONY: binutils
binutils: $(BIN)/$(TARGET)-ld
$(BIN)/$(TARGET)-ld:
	$(MAKE) $(SRC)/$(BINUTILS)/README
	rm -rf $(TMP)/$(BINUTILS) ; mkdir -p $(TMP)/$(BINUTILS) ; cd $(TMP)/$(BINUTILS) ;\
	$(SRC)/$(BINUTILS)/$(CFG) --help > $(TMP)/binutils.configure.help ;\
	$(XPATH) $(SRC)/$(BINUTILS)/$(CFG) $(CFG_BINUTILS) ;\
	$(XMAKE) &&\
	$(MAKE) install &&\
	touch $@ && rm -rf $(SRC)/$(BINUTILS) $(TMP)/$(BINUTILS)

.PHONY: gdb
gdb: $(BIN)/$(TARGET)-gdb
$(BIN)/$(TARGET)-gdb:
	$(MAKE) $(SRC)/$(GDB)/README
	rm -rf $(TMP)/$(GDB) ; mkdir -p $(TMP)/$(GDB) ; cd $(TMP)/$(GDB) ;\
	$(SRC)/$(GDB)/$(CFG) --help > $(TMP)/gdb.configure.help ;\
	$(XPATH) $(SRC)/$(GDB)/$(CFG) $(CFG_GDB) ;\
	$(XMAKE) &&\
	$(MAKE) install &&\
	touch $@ && rm -rf $(SRC)/$(GDB) $(TMP)/$(GDB)

.PHONY: gcc0
gcc0: $(BIN)/$(TARGET)-gcc
$(BIN)/$(TARGET)-gcc:
	$(MAKE) $(SRC)/$(GCC)/README
	rm -rf $(TMP)/$(GCC) ; mkdir -p $(TMP)/$(GCC) ; cd $(TMP)/$(GCC) ;\
	$(SRC)/$(GCC)/$(CFG) --help > $(TMP)/gcc.configure.help ;\
	$(XPATH) $(SRC)/$(GCC)/$(CFG) $(CFG_GCC0) ;\
	$(XMAKE) all-gcc && $(MAKE) install-gcc &&\
	$(XMAKE) all-target-libgcc && $(MAKE) install-target-libgcc &&\
	touch $@ && sync $(SRC)/$(GCC) $(TMP)/$(GCC)

# / <section:gnu>
# \ <section:gz>
GMP_GZ      =      $(GMP).tar.xz
MPFR_GZ     =     $(MPFR).tar.xz
MPC_GZ      =      $(MPC).tar.gz
BINUTILS_GZ = $(BINUTILS).tar.xz
GDB_GZ      =      $(GDB).tar.xz
GCC_GZ      =      $(GCC).tar.xz

.PHONY: gz
gz: $(GZ)/$(GMP_GZ) $(GZ)/$(MPFR_GZ) $(GZ)/$(MPC_GZ) $(GZ)/$(BINUTILS_GZ) $(GZ)/$(GDB_GZ) $(GZ)/$(GCC_GZ)

$(GZ)/$(GMP_GZ):
	$(WGET) -O $@ https://mirror.yandex.ru/mirrors/gnu/gmp/$(GMP_GZ)

$(GZ)/$(MPFR_GZ):
	$(WGET) -O $@ https://mirror.yandex.ru/mirrors/gnu/mpfr/$(MPFR_GZ)

$(GZ)/$(MPC_GZ):
	$(WGET) -O $@ https://mirror.yandex.ru/mirrors/gnu/mpc/$(MPC_GZ)

$(GZ)/$(BINUTILS_GZ):
	$(WGET) -O $@ https://ftp.gnu.org/gnu/binutils/$(BINUTILS_GZ)

$(GZ)/$(GDB_GZ):
	$(WGET) -O $@ https://mirror.yandex.ru/mirrors/gnu/gdb/$(GDB_GZ)

$(GZ)/$(GCC_GZ):
	$(WGET) -O $@ https://mirror.yandex.ru/mirrors/gnu/gcc/gcc-$(GCC_VER)/$(GCC_GZ)
# / <section:gz>
# \ <section:rules>
$(SRC)/%/README: $(GZ)/%.tar.gz
	cd $(SRC) &&  zcat $< | tar x && touch $@
$(SRC)/%/README: $(GZ)/%.tar.bz2
	cd $(SRC) && bzcat $< | tar x && touch $@
$(SRC)/%/README: $(GZ)/%.tar.xz
	cd $(SRC) && xzcat $< | tar x && touch $@
# / <section:rules>
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