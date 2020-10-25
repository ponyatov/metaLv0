## @file
## @brief Phoenix/Elixir stack

# from metaL import *
from elixir import *

class phModule(lxModule):

    def init_apt(self):
        super().init_apt()
        self.apt // 'nodejs' // 'inotify-tools'
        self.apt.sync()

    def init_mk(self):
        super().init_mk()
        self.mk.all //\
            '$(MIX) phx.server'
        self.mk.repl.drop() //\
            '$(IEX) -S $(MIX) phx.server'
        self.mk.sync()

    def init_readme_install(self):
        return super().init_readme_install() //\
            '* https://hexdocs.pm/phoenix/installation.html'

    def init_readme_tutorial(self):
        return super().init_readme_tutorial() //\
            (D('### Phoenix') //
             D() //
             '* Pete Corey [Minimum Viable Phoenix](http://www.petecorey.com/blog/2019/05/20/minimum-viable-phoenix/)' //
             '* José Valim [GOTO 2016 Phoenix a Web Framework for the New Web](https://www.youtube.com/watch?v=bk3icU8iIto)' //
             '* Elixir School [Plug](https://elixirschool.com/ru/lessons/specifics/plug/) /ru/' //
             D()
             )

    # `/mix.exs`
    def init_elixir_mix(self):
        super().init_elixir_mix()
        self.mix.deps //\
            '{:phoenix, "~> 1.5"},' //\
            '{:jason, "~> 1.2"},' //\
            '{:plug_cowboy, "~> 2.4"},'
        self.mix.sync()

    def init_elixir(self):
        super().init_elixir()
        self.ex.mod //\
            (S('def start(mode,opt) do', 'end') //
             'IO.puts("module:<#{__MODULE__}> mode:<#{mode}> opt:<#{opt}>")' //
             '{:ok, self()}'
             )
        self.ex.sync()
        self.init_elixir_web()

    def init_elixir_web(self):
        #
        self.mix.application //\
            f'mod: {{{self:m}.Application, []}},'
        #
        self.ex.endpoint = Section('endpoint')
        self.ex // self.ex.endpoint
        self.ex.endpoint //\
            (S(f'defmodule {self:m}.Endpoint do', 'end') // '')
        #
        self.mix.sync()
        self.ex.sync()

    def init_config(self):
        super().init_config()
        #
        self.config.lx = Dir('config')
        self.diroot // self.config.lx
        self.config.lx.sync()
        #
        self.config.lx.config = exsFile('config')
        self.config.lx // self.config.lx.config
        self.config.lx.config //\
            (D() // 'use Mix.Config') //\
            (D() //
             'config :phoenix, :json_library, Jason' //
             '# config :phoenix, :serve_endpoints, true'
             ) //\
            (D() //
                '# config :exsync, extra_extensions: []' //
                '# config :exsync, src_monitor: false'
             ) //\
            (D() // 'import_config "#{Mix.env()}.exs"')
        #
        self.config.lx.dev = exsFile('dev')
        self.config.lx // self.config.lx.dev
        self.config.lx.dev //\
            (D() // S('use Mix.Config')) //\
            (D() //
             (S(f"config :{self:l}, {self:m}.Endpoint,") //
                f'url: [host: "{self.config.host}"],' //
                f'http: [port: {self.config.port}],' //
                'server: true'
              ))
        #
        self.config.lx.config.sync()
        self.config.lx.dev.sync()
