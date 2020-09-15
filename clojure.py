## @file
## @brief Clojure project template

from metaL import *

## @defgroup clojure
## @ingroup samples
## @brief Clojure project template
## @{

class cljFile(File):
    def __init__(self, V):
        super().__init__(V, ext='.clj', comment=';')

class cljModule(anyModule):

    def __init__(self, V=None):
        super().__init__(V)
        self['clj'] = self.clj = cljFile(self)
        self.diroot // self.clj
        self.clj.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f11.val = 'make repl'
        self.f12.val = 'exit()'
        self.vscode.settings.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.mid // 'repl:\n\tlein repl'
        self.mk.sync()

    def init_apt(self):
        super().init_apt()
        self.apt // 'clojure leiningen'
        self.apt.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext // '"avli.clojure",'
        self.vscode.ext.sync()


MODULE = cljModule()

MODULE['TITLE'] = TITLE = Title('Clojure project template')

MODULE['ABOUT'] = ABOUT = '''
* [Clojure language](https://clojure.org/) workout
  * helloWorld
  * todo
    * web portal
    * metaL port
'''

MODULE['README'] = README = README(MODULE)
diroot = MODULE['dir'] // README
README.sync()

## @}
