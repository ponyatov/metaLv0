# Учебник {#tutru}

см. также <a href=modules.html>модули документации</a> и 
<a href=index.html>главную страницу</a> (README.md)

***

Язык (мета)программирования `metaL` был разработан как смесь Lisp и Python, но не с точки зрения синтаксиса, а духа этих языков.

* *Python* прост в использовании и имеет очень удобный синтаксис
* *Lisp* обладает волшебством самомодификации, способной изменять программу во
  время выполнения, и работать с программой как со структурой данных
* *Smalltalk* это чистый ООП-язык, работающий на основе передачей сообщений,
  которая идеально подходит для распределенных и параллельных систем.

Цель и идеология `metaL` не в написание прикладных программ, а **создание
программ, которые генерируют исходный код других программы** (генерация Си-кода, который может быть скомпилирован и запущен на любой компьютерной системе).

Не пытайтесь написать что-то, что должно быть быстрым, типа числодробилки или
игрового движка -- `metaL` просто так не работает, и быстрое выполнение не предполагалось. Он был создан для манипуляций с программными структурами, и
вы можете писать очень быстрые программы в `metaL`, если вы используете его
правильно: для генерации исходного кода вашего приложения.

***

### Запуск системы

* online-версия: https://repl.it/@metaLmasters/metaL<br>после входа на сайт repl.it дождитесь завершения инициализации песочницы, кликните мышью в командной консоли, и введите команду запуска:
```
Python 3.8.2 (default, Feb 26 2020, 02:56:10)
> bin/python3 -i metaL.py

<vm:metaL> _
```
* локальная установка на собственный компьютер
```sh
~$ git clone -o gh https://github.com/ponyatov/metaL
~$ cd metaL
~/metaL$ make install
```
* интерактивный режим с автоматическим запуском @ref REPL()
```sh
~/metaL$ make metaL/repl
```
* только в Python-режиме: нажмите [Ctrl]+[C] для выхода в интерактивную     
  консоль Python

### `metaL`-скрипт (DDL/DML)

* **используется только однострочный синтаксис** для каждой команды   
  (ограничение функции `input()` в Python)
* выполняется как строка в Python-режиме через функцию @ref metaL()
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
* выполняется интерактивно после запуска @ref REPL()

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
