## @file
## @brief Elixir lang workout

from metaL import *
from elixir import *






MODULE = lxModule()

MODULE['TITLE'] = TITLE = Title('Elixir lang workout')

MODULE['ABOUT'] = ABOUT = '''
* https://elixir-lang.org/getting-started/introduction.html
  * https://elixir-lang.org/getting-started/mix-otp/introduction-to-mix.html
* [Dima Neman **Elixir. Туториал.**](https://www.youtube.com/playlist?list=PLtHDJri4AWWRfOzaQoMQlkWt53aIAPcZ9)
  * [Elixir tutorial - 01 почему elixir? примитивы](https://www.youtube.com/watch?v=9V8-O0yUy1w&list=PLtHDJri4AWWRfOzaQoMQlkWt53aIAPcZ9&index=1)
'''

MODULE['README'] = README = README(MODULE)
MODULE['dir'] // README
README.sync()
