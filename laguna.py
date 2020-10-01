## @file
## @brief distributed guest OS

## @defgroup laguna
## @brief distributed guest OS
## @{

from metaL import *
from dja import *

browser = Window('browser')

class lagModule(djModule):
    def init_templates_index(self):
        super().init_templates_index()
        idx = self.templates.index
        #
        style = Section('style', 0)
        idx.top // "{% block style %}" // style // "{% endblock %}"
        body = Section('body')
        idx.mid // "{% block body %}" // body // "{% endblock %}"
        #
        style // (CSS("*") // 'color:white !important;')
        style // (CSS(".window") //
                  'width:320px; height:240px;' //
                  'min-width:16px; min-height:16px;' //
                  'max-width:640px; max-height:480px;' //
                  'background:#024 !important; border: 2px solid white;' //
                  'resize: both; move: both; overflow: hidden;' //
                  'border-radius: 7px;'
                  )
        body // browser.html() # 
        return idx.sync()


MODULE = lagModule()

MODULE['TITLE'] = TITLE = Title('Laguna: distributed guest OS')

MODULE['ABOUT'] = ABOUT = '''
Business-oriented WebOS built atop of Smalltalk-like language engine:
* Distributed Object DBMS System (DObS)
* Intranet service components
* user-programming paradigm
'''

MODULE['README'] = README = README(MODULE)
MODULE['dir'] // README
README.sync()

## @}
