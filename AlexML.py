## @file
## @brief пример генерации HTML/JS кода по методу `metaL`

from metaL import *

# для настройки нового типа проекта наследуем шаблон проекта-прототипа
class alexModule(anyModule):
    # подправляем .gitignore
    def init_giti(self):
        super().init_giti()
        self.giti.bot // 'LICENSE'
        self.giti.sync() # записать изменения


# создать модуль = каталог /AlexML/
MODULE = alexModule()
# после выполнения строки уже будет создан набор файлов типового проекта: .vscode Makefile apt.txt ...

# создать целевой файл
html = File('index.html', comment=None)
MODULE.diroot // html

# каждый файл имеет 3 секции .top .mid .bot
html.top // '<!DOCTYPE html>'

# с JavaScript работаем так-же: используем универсальные узлы исходного кода S() или наследуюем специальные
script = H('script')
script['type'] = 'text/javascript'
html.bot // script

# корневой элемент
root = H('html')

# сделать push в файл
html.mid // root

head = H('head')
root // head

# 2й параметр H(V,closing=True) указывает что нужно закрывающий тег
charset = H('meta', 0)
charset['charset'] = '"utf8"'
head // charset

# для демонстрации определим спец-класс для тега
class hTitle(H):
    def __init__(self, V):
        super().__init__('title', block=False)
        self // V


title = hTitle(MODULE)
head // title


body = H('body')
root // body

# создаем новый тег
class newTag(H):
    def __init__(self):
        super().__init__('new-tag', closing=True, block=True)
        # запихиваем пример кода как вложенный подграф
        self //\
            (H('a') //
                H('bunch') //
                H('of-old-plain-html', closing=False)
             )


body // newTag()


# записать изменения
html.sync()
