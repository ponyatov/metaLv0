## @file
## @brief Elixir lang target

# from metaL import *
from erlang import *

class exFile(File):
    def __init__(self, V, ext='.ex'):
        super().__init__(V, ext=ext, comment='#', tab='  ')
class exsFile(exFile):
    def __init__(self, V):
        super().__init__(V, ext='.exs')

class lxModule(erlModule):

    def __init__(self, V=None):
        super().__init__(V)
        self.init_elixir()

    def init_elixir(self):
        # lib/.ex
        self.lib = Dir('lib')
        self.diroot // self.lib
        self.lib.sync()
        self.exs = exFile(self)
        self.lib // self.exs
        self.app = Section('app')
        self.exs // (S(f'defmodule {self:t} do', 'end') // self.app)
        # self.app // \
        #     (S('def hello do', 'end') //
        #      ':world')
        self.exs.sync()
        #
        self.init_elixir_config()
        self.init_elixir_formatter()
        self.init_elixir_mix()

    # `config/config.exs`
    def init_elixir_config(self):
        self.config = exsFile('config')
        cfg = Dir('config')
        self.diroot // cfg
        cfg.sync()
        cfg // self.config
        self.config // 'use Mix.Config'
        self.config.sync()

    ## `/.formatter.exs`
    def init_elixir_formatter(self):
        self.formatter = exsFile('.formatter')
        self.diroot // self.formatter
        self.formatter // (S('[', ']') //
                           (S('inputs: [', ']') //
                            '"{config,lib,test}/**/*.{ex,exs}",' //
                            '"{mix,.formatter}.exs"'
                            ))
        self.formatter.sync()

    # `/mix.exs`
    def init_elixir_mix(self):
        self.mix = exsFile('mix')
        self.diroot // self.mix
        self.mix //\
            (S(f"defmodule {self:t}.MixProject do", "end") //
                'use Mix.Project' //
             CR() //
             (S('def project do', 'end') //
              (S('[', ']') //
               f'app: :{self},' //
               'version: "0.0.1",' //
               'elixir: "~> 1.7",' //
               'start_permanent: Mix.env() == :prod,' //
               'deps: deps()'
               )) //
             CR() //
             (S('def application do', 'end') //
              (S('[', ']') //
               'extra_applications: [:logger]'
               )) //
             CR() //
             (S('defp deps do', 'end') // '[]')
             )
        self.mix.sync()

    def init_apt(self):
        super().init_apt()
        self.apt // 'elixir'
        self.apt.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.mid //\
            '/_build/' // 'erl_crash.dump'
        self.giti.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext // '"jakebecker.elixir-ls",' // '"valentin.beamdasm",'
        self.vscode.ext.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f9.cmd .val = 'System.stop'
        self.f12.cmd .val = 'recompile'
        bld = '"**/_build/**":true,'
        els = '"**/.elixir_ls/**":true,'
        self.vscode.watcher // bld // els
        self.vscode.exclude // els
        self.vscode.assoc // '"**/{/**,*}.{ex,exs,app}": "elixir"'
        self.vscode.settings.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.all //\
            (S('.PHONY: all\nall:') //
             '$(MIX) format' //
             '$(MIX) compile')
        self.mk.all //\
            (S('.PHONY: repl\nrepl:') //
             '$(MIX) format' //
             '$(IEX) -S $(MIX)' //
             '$(MAKE) $@')
        self.mk.tools //\
            f'{"IEX":<8} = iex' //\
            f'{"MIX":<8} = mix' //\
            f'{"ELIXIR":<8} = elixir' //\
            f'{"ELIXIRC":<8} = elixirc'
        #
        packs = 'mix local.hex --force'
        self.mk.install // packs
        self.mk.update // packs
        #
        self.mk.sync()
