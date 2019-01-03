#!/usr/bin/env python

import numpy as np
from textwrap import dedent

class PIECE(object):
    def __init__(self, ref_idx=None, ref_arr=None, name=None, shape=None):
        self._ref_idx = ref_idx
        self._ref_arr = ref_arr
        self._name = name
        self._shape = shape

    @property
    def ref_idx(self):
        """
        Return a list of reference array indices
        """
        return self._ref_idx

    @property
    def ref_arr(self):
        """
        Return a list of reference arrays
        """
        return self._ref_arr

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape

    @staticmethod
    def get_ref_rots(start_idx, n_rotations):
        tmp_arr = np.zeros((start_idx.max()+1, start_idx.max()+1), dtype='u1')
        tmp_arr[tuple(start_idx.T)] = 1
        ref_idx = []
        ref_arr = []
        for i in range(n_rotations):
            rot_arr = np.rot90(tmp_arr, -i)
            # Shift array upward if necessary
            while(not np.any(rot_arr[0, :])):
                rot_arr = np.roll(rot_arr, -1, axis=0)
            # Shift array leftward if necessary
            while(not np.any(rot_arr[:, 0])):
                rot_arr = np.roll(rot_arr, -1, axis=1)
            ref_arr.append(rot_arr)
            ref_idx.append(np.argwhere(rot_arr > 0))

        return ref_idx, ref_arr

class RED(PIECE):
    def __init__(self):
        shape = "o-o"
        start_idx = np.array([[0,0], [0,1]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 1)  # Don't rotate!

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='A', shape=shape)

class ORANGE(PIECE):
    def __init__(self):
        shape = dedent("""
                         o  
                        / \ 
                       o   o
                       """)
        start_idx = np.array([[1,0], [0,1], [1,2]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 4)

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='F', shape=shape)

class YELLOW(PIECE):
    
    def __init__(self):
        shape = dedent("""
                       o
                        \ 
                         o
                       """)
        start_idx = np.array([[0,0], [1,1]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 2)  # Only rotate once!

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='B', shape=shape)

class GREEN(PIECE):
    def __init__(self):
        shape = dedent("""
                       o-o
                          \ 
                           o
                       """)
        start_idx = np.array([[0,0], [0,1], [1,2]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 4)

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='C', shape=shape)

class BLUE(PIECE):
    def __init__(self):
        shape = dedent("""
                         o
                         |
                       o-o
                       """)
        start_idx = np.array([[0,1], [1,0], [1,1]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 4)

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='D', shape=shape)

class PURPLE(PIECE):
    def __init__(self):
        shape = dedent("""
                         o
                        / \ 
                       o   o
                       """)
        start_idx = np.array([[0,1], [1,0], [1,2]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 4)

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='E', shape=shape)

class WHITE(PIECE):
    def __init__(self):
        shape = "o"
        ref_idx = np.array([[0,0]])
        ref_idx, ref_arr = self.get_ref_rots(start_idx, 0)

        super().__init__(ref_idx=ref_idx, ref_arr=ref_arr, name='E', shape=shape)

if __name__ == '__main__':
    #red = RED()
    #print(red.ref_arr)
    orange = ORANGE()
    for arr in orange.ref_arr:
        print(arr)
    #yellow = YELLOW()
    #print(yellow.ref_arr)
    #green = GREEN()
    #print(green.ref_arr)
    #blue = BLUE()
    #print(blue.ref_arr)