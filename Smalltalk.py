## @file
## @brief Smalltalk language model /cPython implementation/

from metaL import *

## @defgroup st Smalltalk
## @ingroup samples
## @brief Smalltalk language model /cPython implementation/
## @{

## Smalltalk language/elements
class ST(Meta):
    pass

class stModule(minpyModule):

    def init_mk(self):
        super().init_mk()
        self.mk.all.dropall() //\
            (S('.PHONY: all\nall: $(PY) $(MODULE).py')//
            "bin/pyreverse -o png -p $(MODULE) -f ALL $(MODULE).py ; mv classes_$(MODULE).* doc/"//
            '$^')
        self.mk.sync()

    def init_reqs(self):
        super().init_reqs()
        (self.reqs // 'ply').sync()


MODULE = stModule()

MODULE['TITLE'] = TITLE = Title(
    'Smalltalk language model /cPython implementation/')

Bluebook_pdf = "http://stephane.ducasse.free.fr/FreeBooks/BlueBook/Bluebook.pdf"
ALittleSmalltalk_pdf = "http://sdmeta.gforge.inria.fr/FreeBooks/LittleSmalltalk/ALittleSmalltalk.pdf"

MODULE['ABOUT'] = f'''
* Stéphane Ducasse [Free Online Smalltalk Books](http://stephane.ducasse.free.fr/FreeBooks.html)
  * Adele Goldberg, David Robson, Michael A. Harrison
    **Smalltalk-80: The Language and its Implementation**
    [pdf]({Bluebook_pdf})
  * Timothy Budd
    **A Little Smalltalk**
    [pdf]({ALittleSmalltalk_pdf})
'''

README = README(MODULE)
MODULE['dir'] // README
README // f'![](doc/logo.svg)' // f'![](doc/classes_{MODULE}.png)'
README.sync()


doc = Dir('doc')
MODULE['dir'] // doc
doc.giti = File('.gitignore')
doc // doc.giti
(doc.giti // '*.pdf').sync()

mk = MODULE.mk
gz = Section('doc')
mk.mid // gz
gz // (S(".PHONY: doc\ndoc:", '', '') //
       ' doc/Bluebook.pdf' //
       ' doc/ALittleSmalltalk.pdf' //
       '\n')
gz // (S('doc/Bluebook.pdf:') //
       f"$(WGET) -O $@ {Bluebook_pdf}")
gz // (S('doc/ALittleSmalltalk.pdf:') //
       f"$(WGET) -O $@ {ALittleSmalltalk_pdf}")

mk.install // '$(MAKE) doc'
mk.sync()


py = MODULE.py

model = Section('model')
py.mid // model

## Core `Object`
obj = Class('Object')
model // obj

## `Smalltalk` system
st = Class(MODULE,[obj])
model // st

## Virtual Image p.542
image = Class('Image',[st])
model // image

## Virtual Machine p.542
vm = Class('VM',[st])
model // vm

## Compiler p.542
compiler = Class('Compiler',[st])
model // compiler

## Interpreter p.542
interpreter = Class('Interpreter',[st])
model // interpreter

## Object Memory p.542
memory = Class('Memory',[st])
model // memory

## Hardware HAL p.542
hal = Class('HAL',[st])
model // hal

## Primitive
primitive = Class('Primitive',[obj])
model // primitive

## String p.542
string = Class('String',[primitive])


py.sync()



# ## center method def p.542
# center = stString('center\n\t^ origin + corner / 2')
# print(center.val)

## @name Bytecode
## @{

## Bytecode p.542
class stBytecode(ST):
    pass

## `PUSH` first instance variable p.543
class PUSH_1(stBytecode):
    opcode = 0
## `PUSH` second instance variable p.543
class PUSH_2(stBytecode):
    opcode = 1
## `+` p.543
class ADD(stBytecode):
    opcode = 176
## PUSH SmallInteger(2) p.543
class PUSH_i2(stBytecode):
    opcode = 119
## `/` first p.543
class DIV(stBytecode):
    opcode = 185
## return result p.543
class RET(stBytecode):
    opcode = 124

## @}

## @}
