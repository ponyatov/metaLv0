## @file
## @brief Erlang target

from metaL import *

class erlangFile(File):
    def __init__(self, V, ext='.erl', comment='%'):
        super().__init__(V, ext=ext, comment=comment, tab='  ')

class erlFile(erlangFile):
    def __init__(self, V):
        super().__init__(V, ext='.erl')
        self.export = Tuple()
        self.top //\
            S(f'-module({self.val}).') //\
            (S('-export([', ']).', 0) // self.export) //\
            '-on_load(init/0).'
        self.init = Section('init')
        self.mid // (S('init() ->','.') // self.init)
        self.init //\
            'nil'

class xrlFile(erlangFile):
    def __init__(self, V):
        super().__init__(V, ext='.xrl', comment='%%')
        self.top // '% https://habr.com/ru/post/309382/'
        self.definitions = Section('definitions') // S('Definitions.', '')
        self.rules = Section('rules') // S('Rules.', '')
        self.erlang = Section('erlang') // S('Erlang code.')
        self.top // self.definitions // self.rules // self.erlang
        self.definitions //\
            f'{"D":<3} = [0-9]' //\
            f'{"N":<3} = {{D}}+' //\
            f'{"WS":<3} = [\\s\\t\\r\\n]'
        self.rules //\
            f'{{WS}}+ : skip_token.' //\
            f'.+ : skip_token.'

class erlModule(anyModule):

    def __mixin__(self):
        erlModule.mixin_apt(self)
        erlModule.mixin_mk(self)
        #
        erlModule.init_doc(self)
        self.erl = erlFile(f'{self:l}')
        self.src // self.erl
        self.erl.export // 'hello/0' // 'none/0'
        #io:format("Hello World~n").'
        self.erl.bot //\
            (S('hello() ->') // 'world.') //\
            'none() -> nil.'
        #
        self.erl.sync()

    def __init__(self, V=None):
        super().__init__(V)
        self.__mixin__()
        self.init_erlang()
        self.init_nif()

    def init_erlang(self):
        #
        self.erl //\
            (S('init() ->') //
                f'ok = erlang:load_nif("tmp/{self:l}", 0).')
        # "-compile(export_all)."
        #
        self.erl.sync()

    def init_nif(self):
        self.nif = cFile(f'{self:l}')
        self.src // self.nif
        self.nif //\
            '// http://erlang.org/doc/tutorial/nif.html' //\
            cInclude('erl_nif')
        self.nif //\
            'int foo(int x) { return x*2; }'
        self.nif //\
            (S('static ERL_NIF_TERM foo_nif(ErlNifEnv* env, int argc, const ERL_NIF_TERM argv[]) {', '}') //
             'int x, ret;' //
             (S('if (!enif_get_int(env, argv[0], &x)) {', '}') //
              'return enif_make_badarg(env);') //
             'ret = foo(x);' //
             'return enif_make_int(env, ret);'
             )
        self.nif.funcs = Section('funcs') //\
            '{"foo", 1, foo_nif},'
        self.nif //\
            (S('static ErlNifFunc nif_funcs[] = {', '};') // self.nif.funcs)
        self.nif //\
            f'ERL_NIF_INIT({self:l}, nif_funcs, NULL, NULL, NULL, NULL)'
        self.nif.sync()
        #
        self.mk.test.targets // ' $(TMP)/$(MODULE).so'
        self.mk.rules // (S('$(TMP)/%.so: $(SRC)/%.c') //
                          '$(CC) -fpic -shared -o $@ $<')
        self.mk.sync()
        #
        (self.tmp.giti // '*.so').sync()

    def mixin_apt(self):
        (self.apt // 'erlang').sync()

    def init_apt(self):
        super().init_apt()
        self.mixin_apt()

    def init_giti(self):
        super().init_giti()
        self.giti.mid // '*.dump' // '*.beam'
        self.giti.sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.f9.cmd.val = 'init:stop().'
        self.f12.cmd.val = f'c({self:l}).'
        self.vscode.assoc // '"*.{?rl,core}": "erlang",'
        self.vscode.settings.sync()

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext //\
            '"pgourlain.erlang",' //\
            '"valentin.beamdasm",'
        self.vscode.ext.sync()

    def mixin_doc(self):
        books = {
            'fullbook.pdf': 'https://github.com/dyp2000/Russian-Armstrong-Erlang/raw/master/pdf/',
            'learnyousomeerlang_ru.pdf': 'https://github.com/mpyrozhok/learnyousomeerlang_ru/raw/master/pdf/',
            # 'programming-erlang-2nd-edition.pdf': 'https://gangrel.files.wordpress.com/2015/08/',
            'n2o.pdf': 'https://n2o.dev/books/',
        }
        rename = {
            'fullbook.pdf': 'Programming_Erlang_ru.pdf',
            'learnyousomeerlang_ru.pdf': "Learn_You_Some_Erlang_For_Great_Good_ru.pdf",
        }
        for i, j in books.items():
            k = rename[i] if i in rename else i
            self.mk.doc.doc // S(f' doc/{k}')
            self.mk.doc // (S(f'doc/{k}:') // f'$(WGET) -O $@ {j}{i}')
        self.mk.sync()


    def mixin_mk(self):
        self.mk.tools //\
            f'{"ERL":<8} = erl' //\
            f'{"ERLC":<8} = erlc'
        self.mk.repl.dropall() //\
            f'$(ERL)'
        self.mk.sync()
        erlModule.mixin_doc(self)
        
    def init_mk(self):
        super().init_mk()
        #
        self.mk.rules //\
            (S('%.core: src/%.erl') // '$(ERLC) +to_core $<')
        #
        self.mk.sync()

    def init_readme(self):
        super().init_readme()
        self.readme.tutorial.erlang = \
            (D('\n### Erlang') //
             D() //
             '* [Джо Армстронг об Elixir, Erlang, ФП и ООП](https://habr.com/ru/post/450508/)'
             )
        self.readme.tutorial // self.readme.tutorial.erlang
