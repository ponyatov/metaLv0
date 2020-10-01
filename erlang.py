## @file
## @brief Erlang target

from metaL import *

class erlModule(anyModule):

    def init_apt(self):
        super().init_apt()
        (self.apt // 'erlang').sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext // '"pgourlain.erlang",'
        self.vscode.ext.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.tools //\
            f'{"ERL":<8} = erl' //\
            f'{"ERLC":<8} = erlc'
        self.mk.sync()
