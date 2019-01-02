#!/usr/bin/env python

import scipy.sparse
import numpy as np

class PIECE(object):
    def __init__(self, ref_idx=None, name=None, shape=None):
        self._ref_idx = ref_idx
        self._name = name
        self._shape = shape

    @property
    def ref_idx(self):
        return self._ref_idx

    @ref_idx.setter
    def ref_idxx(self, value):
        self._ref_idx = value

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape

class RED(PIECE):
    def __init__(self):
        shape = "o-o"
        ref_idx = np.array([[0,0], [0,1]])
        super().__init__(ref_idx=ref_idx, name='A', shape=shape)

class ORANGE(PIECE):
    def __init__(self):
        shape = """\
          o  
         / \ 
        o   o
        """
        ref_idx = np.array([[1,0], [0,1], [1,2]])
        super().__init__(ref_idx=ref_idx, name='F', shape=shape)

class YELLOW(PIECE):
    shape = """\
    o
     \ 
      o
    """
    ref_idx = np.array([[0,0], [1,1]])
    def __init__(self):
        super().__init__(ref_idx=ref_idx, name='B', shape=shape)

class GREEN(PIECE):
    def __init__(self):
        shape = """\
        o-o
           \ 
            o
        """
        ref_idx = np.array([[0,0], [0,1], [1,2]])
        super().__init__(ref_idx=ref_idx, name='C', shape=shape)

class BLUE(PIECE):
    def __init__(self):
        shape = """\
          o
          |
        o-o
        """
        ref_idx = np.array([[0,1], [1,0], [1,1]])
        super().__init__(ref_idx=ref_idx, name='D', shape=shape)

class PURPLE(PIECE):
    def __init__(self):
        shape = """\
          o
         / \ 
        o   o
        """
        ref_idx = np.array([[0,1], [1,0], [1,2]])
        super().__init__(ref_idx=ref_idx, name='E', shape=shape)

class WHITE(PIECE):
    def __init__(self):
        shape = "o"
        ref_idx = np.array([[0,0]])
        uper().__init__(ref_idx=ref_idx, name='E', shape=shape)

if __name__ == '__main__':
    red = RED()
    print(red.ref_idx)
    #orange = ORANGE()
    #print(orange.shape)
