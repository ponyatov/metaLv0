# Учебник {#tutru}

### `metaL`-скрипт (DDL/DML)

```py
comment = ' # line comment '
metaL(comment)
#
```
```py
integer = ' -01 # integer '
metaL(integer)
#
# <ast:>
#     <op:-> #f70b8dac @7f131058fe10
#         0: <integer:1> #47696a48 @7f131059d160
#
# <integer:-1> #d85c1811 @7f131058f128
```

### Литералы

Непосредственно можно ввести некоторый набор языковых элементов, которые называются литералами.

* число
```py
number = ' +02.30 # floating point '
metaL(number)
# <number:2.3>
```
```py
integer = ' -01 # integer '
metaL(integer)
# <integer:-1>
```
* строка
```py
simple = " 'single line\n\twith escaped chars' "
metaL(simple)
# <string:single line\n\twith escaped chars>
```
```py
multiline = """ 'multiple lines
\twith escaped chars'
"""
metaL(multiline)
# <string:multiple lines\n\twith escaped chars>
```
* символ: любая группа символов, без пробелов и знаков операторов
```py
symbol = 'MODULE'
metaL(symbol)
# <module:metaL>
```
Тип `Symbol` отличается от других литералов, которые вычисляются сами в себя.
**Символ выполняет поиск в контексте вычисления** аналогично именам переменных в других языках программирования.
```
<vm:metaL> MODULE

<symbol:MODULE> #8b2b5473 @7f54949d8048

<module:metaL> #d80c934b @7f5494ffab38

<vm:metaL> #14ee5988 @7f5494ffa710
        ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7f5494ffabe0
------------------------------------------------------------------
<vm:metaL>
```

### Read-Eval-Print-Loop

*Цикл чтение-вычисление-печать* выполняется в три шага, отдельно для каждой строки исходного кода:

```py
>>> metaL(' -01 \n +2.30 ')

  <ast:>
    <op:-> #f70b8dac @7f01078ac080
      0: <integer:1> #47696a48 @7f01078ac1d0
    <op:+> #63257116 @7f01078ac320
      0: <number:2.3> #c4287bc0 @7f01078ac400
```

1. синтаксический анализ: каждая строка парсится в AST (абстрактное
   синтаксическое дерево) построенное из `metaL`-объектов
   ```
      <op:-> #f70b8dac @7f01078ac080
         0: <integer:1> #47696a48 @7f01078ac1d0
   ```
2. вычисление: объектный граф выполняется через методы `.eval()`/`.apply()`
   ```
      <integer:-1> #d85c1811 @7f905edd3e10
   ```
3. When you run `metaL` scripts via an interactive shell, every line will be
   printed as parsed-only AST and evaluated object, followed by the current VM
   state.
   ```
      <vm:metaL> #14ee5988 @7fc7328d7828
         ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7fc7328d7cf8
         ...
         vm = <vm:metaL> #14ee5988 @7fc7328d7828 _/
   ```
