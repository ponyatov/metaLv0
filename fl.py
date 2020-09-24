## @file
## @brief Flask templates

from metaL import *

## @defgroup fl FL
## @brief Flask templates
## @ingroup web
## @{


class flModule(webModule):

    def init_reqs(self):
        super().init_reqs()
        (self.reqs // 'flask').sync()

    def static_logo(self):
        return "{{ url_for('static', filename='logo.png') }}"

    def init_py(self):
        super().init_py()
        self.init_index()
        self.py.top //\
            pyImport('flask') //\
            f'app = flask.Flask("{self}")'
        self.py.mid //\
            self.index
        self.py.bot //\
            'app.run(host=config.HOST,port=config.PORT,debug=True)'
        self.py.sync()

    def init_index(self):
        self.index = Section('index')
        self.index //\
            "@app.route('/')" //\
            (S('def index():') //
             'return flask.render_template("index.html")'
             )

    def init_vscode_ext(self):
        super().init_vscode_ext()
        self.vscode.ext.ext // '"wholroyd.jinja",'
        self.vscode.ext.sync()


## @}
