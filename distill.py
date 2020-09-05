## @file
## @brief Distilled metaL

from metaL import *

## @defgroup distill distill
## @brief Distilled metaL
## @{

class meModule(minpyModule):
    def __init__(self, V=None):
        super().__init__(V)

MODULE = meModule()

TITLE = Title('Distilled `metaL` / SICP chapter 4 /')
MODULE['TITLE'] = TITLE

ABOUT = '''
* [`metaL` manifest](https://www.notion.so/metalang/metaL-manifest-f7c2e3c9f4494986a620f3a71cf39cff)
* SICP:
  * `.html`ed:
    * https://sarabander.github.io/sicp/html/Chapter-4.xhtml
    * http://zv.github.io/sicp-chapter-4
  * in Clojure: http://www.afronski.pl/sicp-in-clojure/2015/10/05/sicp-in-clojure-chapter-4.html
'''
MODULE['ABOUT'] = ABOUT

GITHUB = Url('https://github.com/ponyatov/metaL/tree/master/')
GITHUB['branch'] = ''
MODULE['GITHUB'] = GITHUB

README = README(MODULE)
MODULE.diroot // README
README.sync()

## @}