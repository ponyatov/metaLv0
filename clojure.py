## @file
## @brief Clojure project template

from metaL import *

## @defgroup clojure
## @brief Clojure project template
## @{

class cljModule(anyModule):

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
