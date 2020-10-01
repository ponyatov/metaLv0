## @file
## @brief VSCode Language Server for live `metaL`

from metaL import *

## @defgroup lsp
## @brief VSCode Language Server for live `metaL`
## @{


class lspModule(anyModule):

    ves = 'vscode-extension-samples'

    samples = {
        'hello': 'helloworld-minimal-sample',
        'lsp-sample': 'lsp-sample',
    }.items()

    def __init__(self, V=None):
        super().__init__(V)
        self.httpd = jsFile('httpd')
        self.diroot // self.httpd
        self.httpd // '''
var http = require('http');
http.createServer(function (req, res) {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World\\n');
}).listen(30000, "127.0.0.1");
console.log('Server running at http://127.0.0.1:30000/');'''
        self.httpd.sync()
        self.init_njs_vscode()
        self.init_njs_package()

    def init_njs_package(self):
        self.package = jsonFile('package')
        self.diroot // self.package
        self.package // (S('{', '}') //
                         f'"name":"{self}",' //
                         f'"description": "{self["TITLE"]}",' //
                         '"version": "0.0.1",' //
                         f'"publisher": "{self["AUTHOR"]}",' //
                         f'"repository": "{self["GITHUB"]}",'//\
                         f'"main":"./{self.extension}"'
                         )
        self.package.sync()

    def init_njs_vscode(self):
        self.extension = jsFile('extension')
        self.diroot // self.extension
        self.extension // "const vscode = require('vscode');"
        self.extension.sync()

    def init_mk(self):
        super().init_mk()
        # self.mk.all // (S('.PHONY:all\nall:')//'node httpd.js')
        self.mk.all // (S('.PHONY:all\nall:') //
                        'npm install' //
                        'npm run compile'
                        )
        self.mk.install //\
            f'-git clone https://github.com/microsoft/{lspModule.ves}.git'
        for loc, ves in lspModule.samples:
            self.mk.install //\
                f'ln -fs {lspModule.ves}/{ves} {loc}'
        self.mk.update //\
            f'cd {lspModule.ves} ; git pull -v origin master'
        self.mk.sync()

    def init_giti(self):
        super().init_giti()
        self.giti.mid //\
            f'/{lspModule.ves}'
        for loc, ves in lspModule.samples:
            self.giti.mid //\
                f'/{loc}'
        self.giti.sync()

    def init_apt(self):
        super().init_apt()
        (self.apt // 'code nodejs').sync()

    def init_vscode_settings(self):
        super().init_vscode_settings()
        self.vscode.watcher //\
            f'"**/{lspModule.ves}/**":true,'
        for loc, ves in lspModule.samples:
            self.vscode.watcher //\
                f'"**/{loc}/**":true,'
        self.vscode.settings.sync()

    def init_vscode_launch(self):
        super().init_vscode_launch()
        self.vscode.launch.it // (S('{', '}') //
                                  '"name": "Run Extension",' //
                                  '"type": "extensionHost",' //
                                  '"request": "launch",' //
                                  '"runtimeExecutable": "${execPath}",' //
                                  '"args": ["--extensionDevelopmentPath=${workspaceFolder}"]')
        self.vscode.launch.sync()


MODULE = lspModule()

MODULE['TITLE'] = TITLE = Title('VSCode Language Server for live `metaL`')
MODULE.init_njs_package()

MODULE['ABOUT'] = ABOUT = '''
VSCode Language Server Protocol (LSP) host that runs `metaL` in a live session:
  * https://code.visualstudio.com/api/language-extensions/language-server-extension-guide
    * https://github.com/microsoft/vscode-extension-samples/tree/master/lsp-sample
parsers:
  * https://tree-sitter.github.io/tree-sitter/
'''

README = README(MODULE)
MODULE['dir'] // README
README.sync()


## @}
