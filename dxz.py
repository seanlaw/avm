#!/usr/bin/env python

from matrix import MATRIX
import numpy as np
from scipy.sparse import csc_matrix
from collections import deque
from functools import lru_cache
from graphillion import GraphSet
from itertools import combinations, chain

class DXZ(object):
    def __init__(self, A, row_labels=None, primary_idx=None):
        self._A = A
        self._row_labels = row_labels
        self._primary_idx = primary_idx
        self._matrix = None
        self._universe = None
        self._gs = None
        self._zdd = None
        self._Z = None

    @property
    def A(self):
        return self._A

    @property
    def matrix(self):
        if self._matrix is None:
            self._matrix = MATRIX(self._A,
                                  self._primary_idx,
                                 )

        return self._matrix

    @property
    def universe(self):
        if self._universe is None:
            n = self.matrix.A.shape[0]
            vertices = list(range(n))
            vertices.append(-1)  # Terminal node
            self._universe = list(combinations(vertices, 2))

        return self._universe

    @property
    def zdd(self):
        if self._zdd is None:
            GraphSet.set_universe(self.universe)            
            self._zdd = GraphSet()

        return self._zdd

    @zdd.setter
    def zdd(self, value):
        self._zdd = value

    @property
    def Z(self):
        if self._Z is None:
            GraphSet.set_universe(self.universe)            
            self._Z = GraphSet()

        return self._Z

    @property
    def solutions(self):
        """
        Returns a generator for each solution stored in the zdd
        """
        for x in iter(self.zdd):
            sol = set(chain(*x))
            sol.remove(-1)  # Remove terminal zdd node
            sol = list(sol)
            if self._row_labels is not None:
                sol = [self._row_labels[row] for row in sol]
            try:
                yield sol
            except StopIteration:
                return

    def _choose_column(self):
        S = np.inf
        for j in self.matrix.h.sweep('R'):
            if j.S < S:
                col = j
                S = j.S

        return col

    def search(self, k=0, level=0):
        if level == 0:
            self.zdd.clear()

        if self.matrix.h.R == self.matrix.h:
            # Empty matrix
            return True

        c = self._choose_column()
        x = False
        self.matrix.cover(c)
        for r in c.sweep('D'):
            Ok = r
            for j in r.sweep('R'):
                self.matrix.cover(j.column)
            y = self.search(k+1, level+1)
            #if not y is False:
            #    x = self.unique(r.row, y)
            if y is True:
                x = GraphSet([[(r.row, -1)]])
            elif isinstance(y, GraphSet):
                x = GraphSet([[(r.row, -1)]]).join(y)
                if level == 0:
                    if len(self.zdd) == 0:
                        self.zdd.update(x)
                    else:
                        self.zdd = self.zdd.union(x)

            r = Ok
            c = r.column
            for j in r.sweep('L'):
                self.matrix.uncover(j.column)

        self.matrix.uncover(c)

        return x

    def unique(self, r, y):
        return r

if __name__ == "__main__":
    # ZDD Example
    arr = np.array([[1, 1, 1, 0, 1, 0],
                    [1, 1, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 1],
                    [0, 0, 1, 1, 0, 1],
                    [0, 0, 1, 0, 1, 0],
                   ], dtype='u1')

    csc = csc_matrix(arr)
    row_labels = list(range(1, csc.shape[0]+1))
    dxz = DXZ(csc, row_labels)
    dxz.search()
    for sol in dxz.solutions:
        print(sol)