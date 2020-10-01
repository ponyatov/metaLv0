## @file
## @brief Live View web hacking

# from metaL import *
from phoenix import *

class lvModule(phModule):

    def init_apt(self):
        super().init_apt()
        self.apt // 'nodejs'
        self.apt.sync()


MODULE = lvModule()

MODULE['TITLE'] = TITLE = Title('Live View web hacking')

MODULE['ABOUT'] = ABOUT = '''
* https://github.com/dwyl/phoenix-liveview-counter-tutorial
  * https://alchemist.camp/episodes/phoenix-live-view-setup
    * https://alchemist.camp/episodes/asdf-language-versions
  * https://hexdocs.pm/phoenix/installation.html
* https://hexdocs.pm/phoenix/installation.html
* YouTube
  * [Phoenix LiveView for web developers who don't know Elixir](https://www.youtube.com/watch?v=U_Pe8Ru06fM)
'''

README = README(MODULE)
MODULE['dir'] // README
README.sync()
