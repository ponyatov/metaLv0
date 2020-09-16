## @file
## @brief WebRTC-based distributed computing platform (JS hell)

from metaL import *

## @defgroup wrtc WebRTC-OS
## @ingroup os
## @brief WebRTC-based distributed computing platform (JS hell)
## @{

TITLE = Title('WebRTC-based distributed computing platform (JS hell)')

ABOUT = '''
* Hans Oksendahl http://hox.io/
  * [Bubble Hash is a distributed hash-table implemented in a web browser](https://github.com/hansoksendahl/bubblehash)
    * issue [WebRTC is an interesting technology for distributed OS design](https://github.com/hansoksendahl/bubblehash/issues/1)
      * https://www.unisonweb.org/talks ideas about global hashed objects storage
'''

## [D]istributed [S]ystem Module
class dsModule(minpyModule):

    def __init__(self, V=None):
        super().__init__(V)
        self.init_ini()

    def init_ini(self):
        self['ini'] = self.ini = File(self, ext='.ini')
        self.diroot // self.ini
        self.ini.sync()

    def init_reqs(self):
        super().init_reqs()
        self.reqs // 'flask' // 'ply' // 'xxhash'
        self.reqs.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.all.dropall() //\
            (S('all: $(PY) $(MODULE).py $(MODULE).ini') //
                "$^")
        self.mk.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f11.cmd.val = 'make test'
        self.f12.cmd.val = 'make all'
        self.vscode.settings.sync()

    def init_py(self):
        super().init_py()
        #
        self['parser'] = self.parser = Section('parser')
        self.py // self.parser
        self.parser //\
            pyImport('ply.lex  as lex') //\
            pyImport('ply.yacc as yacc')
        #
        self['web'] = self.web = Section('web interface')
        self.py // self.web
        self.web //\
            pyImport('flask')
        #
        self.py.sync()


MODULE = dsModule()

MODULE['TITLE'] = TITLE
MODULE['ABOUT'] = ABOUT

README = README(MODULE)
diroot = MODULE['dir'] // README
README.sync()

## @}
