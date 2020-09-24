## @file
## @brief `HTML` markdown objects

from metaL import *

## @defgroup tags tags
## @ingroup html
## @brief `HTML` markdown objects
## @{

class A(H):
    def __init__(self, href, *vargs, **kwargs):
        super().__init__('A', *vargs, **kwargs)
        self['href'] = Url(href)
        self.block = False

class EMAIL(H):
    def __init__(self, email, *vargs, **kwargs):
        super().__init__('A', *vargs, **kwargs)
        self['href'] = f'mailto:{email}'
        self // f'{email}'
        self.block = False

    def file(self, depth=0):
        ret = super().file(depth)
        return f'&LT;{ret}&GT;'

class IMG(H):
    def __init__(self, src, *vargs, **kwargs):
        super().__init__('IMG', 0, *vargs, **kwargs)
        self['src'] = src
        self.block = False

class HH(H):
    ## param[in] V optional sub-content
    def __init__(self, V=None, *vargs, **kwargs):
        super().__init__(self.__class__.__name__, *vargs, **kwargs)
        self.block = False
        if V:
            self // V
class HB(HH):
    def __init__(self, V=None, *vargs, **kwargs):
        super().__init__(V, *vargs, **kwargs)
        self.block = True


class CSS(S):
    def __init__(self, start, block):
        start = '%s {' % f'{start:<22}'
        end = '}'
        if not block:
            start += ' '
            end = ' ' + end
        super().__init__(start, end, block)

## @name table
## @{

class TABLE(HB):
    pass
class TR(HB):
    pass
class TD(HB):
    pass

## @}


class STATIC(S):
    def __init__(self, filename, *vargs, **kwargs):
        super().__init__('{%% static "%s" %%}' % filename)

class PX(S, Integer):

    def __init__(self, size, *vargs, **kwargs):
        assert isinstance(size, int)
        S.__init__(self, size)

    def __format__(self, spec=None):
        assert not spec and isinstance(self.val, int)
        return f'{self.val}px'


class HR(H):
    def __init__(self):
        super().__init__('HR', 0)

class CENTER(HH):
    pass
class SPAN(HH):
    pass
class DIV(HB):
    pass
    # def __init__(self, *vargs, **kwargs):
   #     super().__init__('DIV', *vargs, **kwargs)

class P(HB):
    def __init__(self, V=None, *vargs, **kwargs):
        super().__init__(V, *vargs, **kwargs)
        self.block = False

class H1(HH):
    pass
class H2(HH):
    pass
   # def __init__(self, V, *vargs, **kwargs):
  #     super().__init__('H1', *vargs, **kwargs)
  #     self.block = False
  #     self // V

## @}
