## @file
## @brief Smalltalk model

from metaL import *

## @defgroup st Smalltalk
## @brief model
## @{

## Smalltalk elements
class ST(Object):
    pass

## Virtual Image p.542
class stImage(ST):
    pass

## Virtual Machine p.542
class stVM(ST):
    pass

## Compiler p.542
class stCompiler(ST):
    pass

## Interpreter p.542
class stInterpreter(ST):
    pass

## Object Memory p.542
class stMemory(ST):
    pass

## Hardware HAL p.542
class stHAL(ST):
    pass

## String p.542
class stString(ST, String):
    pass


## center method def p.542
center = stString('center\n\t^ origin + corner / 2')
print(center.val)

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
