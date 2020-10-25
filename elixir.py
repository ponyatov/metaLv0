## @file
## @brief Elixir lang target

# from metaL import *
from erlang import *

class exFile(File):
    def __init__(self, V, ext='.ex'):
        super().__init__(V, ext=ext, comment='#', tab='  ')
        if self.__class__ == exFile:
            self.top // 'require Logger'
class exsFile(exFile):
    def __init__(self, V):
        super().__init__(V, ext='.exs')

class exModule(erlModule):

    def __init__(self, V=None):
        super().__init__(V)
        self.init_elixir()

    def __mixin__(self):
        erlModule.__mixin__(self)
        # exModule.mixin_apt(self)
        # exModule.mixin_giti(self)
        # exModule.mixin_mk(self)
        # exModule.mixin_elixir(self)
        # # exModule.mix_deps(self)
        # exModule.mixin_doc(self)
        # # self.mix_deps()

    def mixin_doc(self):
        erlModule.mixin_doc(self)

    def __format__(self, spec):
        if spec == 'm':
            return f'{self:t}'
        else:
            return super().__format__(spec)

    def init_elixir_lib(self):
        self.lib = Dir('lib')
        self.diroot // self.lib
        self.lib.sync()
        self.ex = exFile(f'{self:l}')
        self.lib // self.ex
        self.ex.mod = Section('mod')
        self.ex //\
            (S(f'defmodule {self:m} do', 'end') //
             self.ex.mod)
        self.ex.sync()
        #
        # self.lib.mod = Dir(f'{self:l}')
        # self.lib // self.lib.mod
        # self.lib.mod.sync()
        self.lib.app = exFile('application')
        self.lib // self.lib.app
        self.lib.app.opts = S('', block=False) //\
            'strategy: :one_for_one,' //\
            f' name: {self:m}.Supervisor'
        self.lib.app.mod = Section('module')
        self.lib.app.start = Section('start')
        self.lib.app //\
            (S(f'defmodule {self:m}.Application do', 'end') //
             '@moduledoc false' //
             'use Application' //
             CR() //
             (S('def start(_type, _args) do', 'end') //
                (S('children = [', ']') //
                 '# Starts a worker by calling: Camp.Worker.start_link(arg)' //
                 f'# {{{self:m}.Worker, arg}}'
                 ) //
                 self.lib.app.start //
                (S('opts = [', ']', block=False) // self.lib.app.opts) //
                'Supervisor.start_link(children, opts)'
              ) //
             self.lib.app.mod
             )
        self.lib.app.sync()

    def mixin_cowboy(self):
        self.mix.deps // '{:cowboy, "~> 1.0.0"},'
        self.mix.apps // ':cowboy'
        self.mix.sync()
        #
        self.lib.app.start // f'{self:m}.Web.cowboy'
        self.lib.web = exFile('web')
        self.lib // self.lib.web
        self.lib.web.mod = Section('mod')
        self.lib.web.router = Section('router') //\
            (S('def call(path, req, state) do', 'end') //
             'Logger.info  inspect(path: path)' //
             'Logger.debug inspect(req: req)' //
             'Logger.debug inspect(state: state)' //
             'route(path, req, state)')
        self.lib.web.mid //\
            (S(f'defmodule {self:m}.Web do', 'end') //
                self.lib.web.mod) //\
            (S(f'defmodule {self:m}.Web.Router do', 'end') //
                self.lib.web.router)
        self.lib.web.mod //\
            f'@port {self.config.port}' //\
            '@procs 0x10' //\
            (S('def cowboy do', 'end') //
             'host = :_' //
             'anyroute = {:_, __MODULE__, []}' //
             'dispatch = :cowboy_router.compile([{host, [anyroute]}])' //
             'opts = [port: @port]' //
             'env = [dispatch: dispatch]' //
             (S('case :cowboy.start_http(:http, @procs, opts, [env: env]) do', 'end') //
                 '{:ok, _pid} -> Logger.info "Cowboy runs @ http://localhost:#{@port}"' //
                 'err -> Logger.error "Cowboy error #{inspect(err)}"'
              )
             )
        #
        self.lib.web.init = Section('init') //\
            '{:ok, req, state}'
        self.lib.web.handle = Section('handle') //\
            '{path, req} = :cowboy_req.path(req)' //\
            'headers = [{"content-type", "text/html"}]' //\
            f"{{:ok, resp}} = :cowboy_req.reply(200, headers, {self:m}.Web.Router.call(path, req, state), req)" //\
            '{:ok, resp, state}'
        self.lib.web.terminate = Section('terminate') //\
            ':ok'
        #
        self.lib.web.style = Section('style') //\
            '''
    defp style, do: """
        <style>
        pre {
        white-space: pre-wrap;
        word-break: keep-all
        }
        </style>
        """


'''
        self.lib.web.router //\
            self.lib.web.style //\
            (S('defp route(path, req, state) do', 'end') //
                '''
    """
    #{style()}
    <hr>
    <pre>#{inspect(path)}</pre>
    <hr>
    <pre>#{inspect(req)}</pre>
    <hr>
    <pre>#{inspect(state)}</pre>
    """
            ''')
        #
        self.lib.web.mod //\
            (S('def init({:tcp, :http}, req, state) do', 'end') //
             self.lib.web.init) //\
            (S('def handle(req, state) do', 'end') //
             self.lib.web.handle) //\
            (S('def terminate(_reason, _req, _state) do', 'end') //
             self.lib.web.terminate)
        #
        self.lib.app.sync()
        self.lib.web.sync()

    def mixin_elixir(self):
        #
        exModule.mixin_apt(self)
        exModule.mixin_giti(self)
        exModule.mixin_mk(self)
        exModule.mixin_vscode_settings(self)
        # lib/.ex
        exModule.init_elixir_lib(self)
        #
        exModule.init_elixir_test(self)
        exModule.init_elixir_formatter(self)
        exModule.init_elixir_mix(self)

    def init_elixir(self):
        self.mixin_elixir()

    ## `/test`
    def init_elixir_test(self):
        self.diroot.test = Dir('test')
        self.diroot // self.diroot.test
        self.test_helper = (exsFile('test_helper') // 'ExUnit.start()')
        self.diroot.test // self.test_helper
        self.test_helper.sync()
        #
        self.test = exsFile(f'{self:l}_test')
        self.diroot.test // self.test
        self.test.it = Section('test')
        self.test //\
            (S(f'defmodule {self:m}Test do', 'end') //
             'use ExUnit.Case' //
             f'doctest {self:m}' //
             self.test.it)
        self.test.sync()

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

    def mix_deps(self):
        self.mix.deps //\
            '# {:exsync, "~> 0.2", only: :dev},'
        self.mix.sync()

    # `/mix.exs`
    def init_elixir_mix(self):
        self.mix = exsFile('mix')
        self.diroot // self.mix
        self.mix.project = Section('project') //\
            f'app: :{self:l},' //\
            'version: "0.0.1",' //\
            'elixir: "~> 1.5",' //\
            f'name: "{self}",' //\
            f'description: "{self["TITLE"]}",' //\
            f'source_url: "{self["GITHUB"]}",' //\
            'start_permanent: Mix.env() == :prod,' //\
            'docs: [extras: ["README.md"]],' //\
            'package: package(),' //\
            'deps: deps()'
        self.mix.application = Section('application')
        self.mix.deps = Section('deps')
        self.mix.apps = Section('apps')
        self.mix.mod = f'mod: {{{self:m}.Application, []}},'
        self.mix.extra = Section('extra') // ':logger'
        package = (D() // (S('defp package do', 'end') //
                           (S('[', ']') //
                            f'name: "{self:l}",' //
                            'files: ~w(lib src .formatter.exs mix.exs README* LICENSE*),' //
                            f'licenses: ["{self.LICENSE.val.split()[0]}"],' //
                            f'links: %{{"GitHub" => "{self["GITHUB"]}"}},' //
                            f'maintainers: ["{self.AUTHOR} {self.EMAIL}"]'
                            )))
        self.mix //\
            (S(f"defmodule {self:t}.MixProject do", "end") //
                'use Mix.Project' //
             CR() //
             (S('def project do', 'end') //
              (S('[', ']') //
               self.mix.project
               )) //
             CR() //
             (S('def application do', 'end') //
              (S('[', ']') //
               self.mix.mod //
               self.mix.application //
               (S('applications: [', '],') //
                self.mix.apps) //
               (S('extra_applications: [', ']') //
                self.mix.extra)
               )) //
             CR() //
             (S('defp deps do', 'end') //
              (S('[', ']') //
               self.mix.deps //
               '{:ex_doc, ">= 0.0.0", only: :dev, runtime: false}'
               )) //
             package
             )
        self.mix.sync()

    def mixin_apt(self):
        self.apt // 'elixir'
        self.apt.sync()

    def init_apt(self):
        super().init_apt()
        self.mixin_apt()
        # self.apt // 'inotify-tools'

    def mixin_giti(self):
        self.giti.mid //\
            '/deps/' //\
            '/*.lock' //\
            '/_build/' //\
            'erl_crash.dump'
        self.giti.bot //\
            '/doc/'
        self.giti.sync()

    def init_giti(self):
        super().init_giti()
        self.mixin_giti()

    def init_readme(self):
        super().init_readme()
        self.readme.tutorial.elixir = \
            (D('\n### Elixir') //
             D() //
             '* https://elixirschool.com/' //
             (S('* https://elixir-lang.org/getting-started/introduction.html') //
              '* https://elixir-lang.org/getting-started/mix-otp/introduction-to-mix.html') //
             '* [Курс Elixir](https://www.youtube.com/playlist?list=PLCZmBMhe5aeiukyPrbOv6otgy55ZTfcgd)' //
             '* Dima Neman [Elixir. Туториал.](https://www.youtube.com/playlist?list=PLtHDJri4AWWRfOzaQoMQlkWt53aIAPcZ9)' //
             '* [Elixir School](https://elixirschool.com/ru/) /ru/'
             )
        self.readme.tutorial // self.readme.tutorial.elixir
        self.readme.preinstall //\
            f'copy required `mix.exs` deps from: https://hex.pm/packages/{self:l}'

    def init_readme_tutorial(self):
        return super().init_readme_tutorial() //\
            self.readme.tutorial.elixir

    def mixin_mk(self):
        self.mk.tools //\
            f'{"IEX":<8} = iex' //\
            f'{"MIX":<8} = mix' //\
            f'{"ELIXIR":<8} = elixir' //\
            f'{"ELIXIRC":<8} = elixirc'
        self.mk.test //\
            '$(MIX) format' //\
            '$(MIX) test'
        self.mk.repl.dropall() //\
            '$(IEX)  -S $(MIX)'
        #
        mixget = '$(MIX)  deps.get'
        mxcmpl = '$(MIX)  compile'
        self.mk.install // mixget // mxcmpl
        self.mk.update // mixget // mxcmpl
        #
        self.mk.merge // 'MERGE += lib .formatter.exs mix.exs'
        #
        self.mk.sync()

    def init_mk(self):
        super().init_mk()
        self.mixin_mk()

    def mixin_vscode_ext(self):
        self.vscode.ext.ext //\
            '"jakebecker.elixir-ls",'
        self.vscode.ext.sync()
        # '"mjmcloug.vscode-elixir",' //\ not compat with jakebecker
        # '"sammkj.vscode-elixir-formatter",'

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.mixin_vscode_ext()
        # '"royalmist.vscode-eex-format",' //\

    def mixin_vscode_settings(self):
        self.f9.cmd .val = 'System.stop'
        self.f12.cmd .val = 'recompile'
        bld = '"**/_build/**":true,'
        deps = '"**/deps/**":true,'
        els = '"**/.elixir_ls/**":true,'
        self.vscode.watcher // bld // deps // els
        self.vscode.exclude // bld // deps // els
        self.vscode.assoc // '"*.{ex,exs,app}": "elixir"'
        self.vscode.settings.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.mixin_vscode_settings()


class phModule(exModule):

    def init_elixir_web(self):
        self.lib.web = exFile('web')
        self.lib // self.lib.web
        self.lib.web.mid //\
            (Section('endpoint') //
             (S('defmodule Web.Endpoint do', 'end') //
              (D() //
               'use Application' //
               'require Logger' //
               'use Phoenix.Endpoint, otp_app: :web'
               ) //
              (D() // (S('def start(type, opts) do', 'end') //
                       'Logger.info("#{__MODULE__}: #{type} / #{opts}")' //
                       'Supervisor.start_link([__MODULE__], strategy: :one_for_one)'
                       )) //
              (D() //
               'plug(Web.Router)')
              ))
        self.lib.web.mid //\
            (Section('endpoint') //
             (S('defmodule Web.Router do', 'end') //
              'use Phoenix.Router' //
              'get("/", Web.IndexController, :index)'
              ))
        self.lib.web.mid //\
            (Section('controller') //
             (S('defmodule MinimalWeb.HomeController do', 'end') //
                 'use Phoenix.Controller, namespace: Web' //
              (S('def index(conn,params) do', 'end') //
               'Phoenix.Controller.html(conn,"<pre>#{conn} #{params}</pre>")')
              )
             )
        self.lib.web.bot // '''
# # https://habr.com/ru/post/306334/
#   import Plug.Conn

#   def init(opts) do
#     Map.put(opts, :my_option, "Hello")
#     opts
#   end

#   def call(conn, opts) do
#     conn |> send_resp(200, "Hello World!\\n<pre>#{opts}</pre>")
#   end'''
        #
        self.lib.web.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        # self.vscode.ext.ext //\
        #     '"mjmcloug.vscode-elixir",' //\
        #     '"sammkj.vscode-elixir-formatter",'
        # self.vscode.ext.sync()
        # # '"royalmist.vscode-eex-format",' //\
        # # '"jakebecker.elixir-ls",' //\ ver 1.8 reqs & red lines in .exs

    def init_readme_tutorial(self):
        return super().init_readme_tutorial() + '''
* https://elixir-lang.org/getting-started/introduction.html
  * https://elixir-lang.org/getting-started/mix-otp/introduction-to-mix.html
* [Курс Elixir](https://www.youtube.com/playlist?list=PLCZmBMhe5aeiukyPrbOv6otgy55ZTfcgd)
* Dima Neman [Elixir. Туториал.](https://www.youtube.com/playlist?list=PLtHDJri4AWWRfOzaQoMQlkWt53aIAPcZ9)

### Phoenix

* http://twentyeighttwelve.com/creating-a-phoenix-framework-application-with-sqlite/
'''
