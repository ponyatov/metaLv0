## @file
## @brief Cross-Compiler toolchain build from source

from metaL import *

## @defgroup cross
## @ingroup os
## @brief Cross-Compiler toolchain build from source
## @{

## hardware
class HW(Object):
    def __format__(self, spec):
        assert not spec
        return f'{self.val}'

class ARCH(HW):
    pass


i386 = ARCH('i386')

class TARGET(HW):
    def file(self, depth=0):#, parent=None
        return f'{self}'

class CPU(HW):
    def __init__(self, V):
        super().__init__(V)
        self['target'] = self.target = TARGET('i486-elf')


i486dx = CPU('i486dx')
i486dx['arch'] = i486dx.arch = i386


class QEMU(HW):
    def __init__(self, V='386', cpu=i486dx):
        super().__init__(V)
        if V == '386':
            self['cpu'] = self.cpu = cpu
            self['target'] = self.target = cpu.target
        else:
            raise Error((V))

    def __format__(self, spec):
        assert not spec
        return f'{self._type()}{self.val}'


qemu386 = QEMU()


## packages list
cclibs = {
    'gmp': '6.2.0',
    'mpfr': '4.1.0',
    'mpc': '1.2.0',
}
gnu = {
    'binutils': '2.35.1',
    'gdb': '9.2',
    'gcc': '9.3.0'
}
pkg = {}
pkg.update(cclibs)
pkg.update(gnu)

## [T]arget [C]ompiler
class tcModule(anyModule):

    def init_first(self):
        super().init_first()
        self['hw'] = self.hw = qemu386
        self['cpu'] = self.cpu = i486dx
        self['arch'] = self.arch = self.cpu.arch
        self['target'] = self.target = self.cpu.target

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f12.cmd.val = 'make gmp'
        for p in pkg:
            t = f'"**/tmp/{p}-*/*":true,'
            h = f'"**/tmp/{p}.configure.help":true,'
            s = f'"**/src/{p}-*/*":true,'
            ts = f'{t:<28}{s}'
            self.vscode.watcher // ts
            self.vscode.exclude // ts
        self.vscode.watcher //\
            f'"**/{self.target}/**":true,' //\
            f'"**/firmware/**":true,'
        self.vscode.settings.sync()

    def init_dirs(self):
        super().init_dirs()
        self.fw = Dir('firmware')
        self.diroot // self.fw
        self.fw.giti = (File('.gitignore') //
                        '*.iso' // '*.elf' //
                        '*.bin' // '*.hex' //
                        '*.kernel' // '*.rootfs')
        self.fw // self.fw.giti
        self.fw.giti.sync()
        self.tmp.giti // '*.configure.help'
        self.tmp.giti.sync()
        self.target['dir'] = self.target.dir = Dir(self.target)
        self.diroot // self.target.dir
        self['root'] = self.root = Dir('root')
        self.target.dir // self.root

    def init_mk(self):
        super().init_mk()
        #
        self.mk.dirs //\
            f'{"GZ":<8} = $(HOME)/gz' //\
            f'{"PFX":<8} = $(CWD)/$(TARGET)' //\
            f'{"BIN":<8} = $(PFX)/bin' //\
            f'{"LIB":<8} = $(PFX)/lib' //\
            f'{"ROOT":<8} = $(PFx)/root' //\
            f'{"FW":<8} = $(CWD)/firmware'
        #
        self.mk.module //\
            f'{"APP":<8} = {self}' //\
            f'{"HW":<8} = {self.hw}' //\
            f'{"CPU":<8} = {self.cpu}' //\
            f'{"ARCH":<8} = {self.arch}' //\
            f'{"TARGET":<8} = {self.target}'
        # cross/packages
        cross = Section('cross')
        packages = Section('packages')
        self.mk.version // cross
        self.mk.mid // packages
        for p in pkg:
            pack = f'{p.upper()}_VER'
            ver = f'{pkg[p]}'
            cross // f'{pack:<12} = {ver}'
            packages // f'{p.upper():<8} = {p.lower():>8}-$({p.upper()}_VER)'
            pv = f'{p}-*/'
            self.tmp.giti // pv
            self.src.giti // pv
        self.tmp.giti.sync()
        self.src.giti.sync()
        # #
        # self.mk.mid // packs
        # for p in pkg:
        #     packs //
        # cfg
        cfg = Section('cfg')
        self.mk.mid // cfg
        cfg //\
            f'{"CFG":<12} = configure --prefix=$(PFX)' //\
            f'{"CFG_CCLIBS":<12} = --disable-shared ' //\
            f'{"CFG_GMP":<12} = $(CFG_CCLIBS)' //\
            f'{"CFG_MPFR":<12} = $(CFG_CCLIBS)' //\
            f'{"CFG_MPC":<12} = $(CFG_CCLIBS) --with-mpfr=$(PFX)' //\
            (S(f'{"CFG_BINUTILS":<12} = \\') //
             '--target=$(TARGET) \\' //
             '--with-sysroot=$(ROOT) --with-native-system-header-dir=/include \\' //
             '--enable-lto --disable-multilib \\' //
             '--disable-nls'
             ) //\
            f'{"CFG_GDB":<12} = $(CFG_BINUTILS)' //\
            (S(f'{"CFG_GCC":<12} = $(CFG_BINUTILS) \\') //
             '--enable-languages="c" \\' //
             '--with-gmp=$(PFX) --with-mpfr=$(PFX) --with-mpc=$(PFX)'
             ) //\
            f'{"CFG_GCC0":<12} = $(CFG_GCC) --without-headers --with-newlib' //\
            ''
        # cross
        cross = Section('cross') // '.PHONY: cross\ncross: cclibs gnu'
        ccl = Section('cclibs') // '.PHONY: cclibs\ncclibs: gmp mpfr mpc' // ''
        gnus = Section('gnu') // '.PHONY: gnu\ngnu: binutils gdb gcc0' // ''
        self.mk.mid // cross // ccl // gnus

        def genpack(p0, l, make='$(XMAKE)', install='$(MAKE) install', clean='rm -rf'):
            p = re.sub(r'\d$', r'', p0)
            assert p in pkg
            s = f'$(SRC)/$({p.upper()})'
            t = f'$(TMP)/$({p.upper()})'
            return (Section(p, 0) //
                    f'.PHONY: {p0}' //
                    f'{p0}: {l}' //
                    (S(f'{l}:') //
                     f'$(MAKE) {s}/README' //
                     f'rm -rf {t} ; mkdir -p {t} ; cd {t} ;\\' //
                     f'{s}/$(CFG) --help > $(TMP)/{p}.configure.help ;\\' //
                     f'$(XPATH) {s}/$(CFG) $(CFG_{p0.upper()}) ;\\' //
                     f'{make} &&\\' //
                     f'{install} &&\\' //
                     f'touch $@ && {clean} {s} {t}'
                     ))
        ## cclibs
        for p in cclibs:
            ccl // genpack(p, f'$(LIB)/lib{p}.a')
        # gnu
        gnus //\
            genpack('binutils', f'$(BIN)/$(TARGET)-ld') //\
            genpack('gdb', f'$(BIN)/$(TARGET)-gdb') //\
            genpack('gcc0', f'$(BIN)/$(TARGET)-gcc',
                    make='$(XMAKE) all-gcc && $(MAKE) install-gcc',
                    install='$(XMAKE) all-target-libgcc && $(MAKE) install-target-libgcc',
                    clean='sync')

        # gz
        gz = Section('gz')
        self.mk.mid // gz
        for p in pkg:
            if p in ['mpc']:
                ext = 'gz'
            else:
                ext = 'xz'
            gz // f'{p.upper()+"_GZ":<11} = {"$("+p.upper()+")":>11}.tar.{ext}'
        #
        makegz = S('\n.PHONY: gz\ngz:', '', 0)
        gz // makegz
        for p in pkg:
            makegz // f' $(GZ)/$({p.upper()}_GZ)'
        #
        urls = {
            'binutils': 'https://ftp.gnu.org/gnu/binutils',
            'gcc': 'https://mirror.yandex.ru/mirrors/gnu/gcc/gcc-$(GCC_VER)',
            'gdb': 'https://mirror.yandex.ru/mirrors/gnu/gdb',
            'gmp': 'https://mirror.yandex.ru/mirrors/gnu/gmp',
            'mpfr': 'https://mirror.yandex.ru/mirrors/gnu/mpfr',
            'mpc': 'https://mirror.yandex.ru/mirrors/gnu/mpc'
        }
        for p in pkg:
            gz // f'\n$(GZ)/$({p.upper()}_GZ):\n\t$(WGET) -O $@ {urls[p]}/$({p.upper()}_GZ)'
        #
        rules = Section('rules')
        self.mk.mid // rules
        arch = {'gz': 'zcat', 'bz2': 'bzcat', 'xz': 'xzcat'}
        for xz in arch:
            rules // f'$(SRC)/%/README: $(GZ)/%.tar.{xz}\n\tcd $(SRC) && {arch[xz]:>5} $< | tar x && touch $@'
        #
        self.mk.sync()

    def init_apt(self):
        super().init_apt()
        self.apt // 'build-essential bzip2 xz-utils'
        self.apt.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.mid // f'/{self.target}/'
        self.giti.sync()


MODULE = tcModule()

MODULE['TITLE'] = TITLE = Title('Cross-Compiler toolchain build from source')
MODULE['ABOUT'] = ABOUT = '''
build custom GCC toolchain
'''

README = README(MODULE)
MODULE['dir'] // README
README.sync()


## @}
