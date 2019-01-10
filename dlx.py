#!/usr/bin/env python

from matrix import MATRIX
import numpy as np
from scipy.sparse import csc_matrix

class DLX(object):
    def __init__(self, A):
        self._A = A

        self._matrix = None
        self._rows = None
        self._cols = None
        self._h = None

    @property
    def A(self):
        return self._A

    @property
    def matrix(self):
        if self._matrix is None:
            self._matrix = MATRIX(self.A)

        return self._matrix

    @property
    def rows(self):
        return self._rows

    @property
    def cols(self):
        return self._cols

    @property
    def h(self):
        if self._h is None:
            pass

        return self._h


if __name__ == "__main__":
    arr = np.array([[0, 0, 1, 0, 1, 1, 0],
                    [1, 0, 0, 1, 0, 0, 1],
                    [0, 1, 1, 0, 0, 1, 0],
                    [1, 0, 0, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 1, 0, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)

    dlx = DLX(csc)
    dlx.matrix