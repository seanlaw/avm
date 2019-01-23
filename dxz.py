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
        self._zdd = None

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
    def zdd(self):
        if self._zdd is None:
            self._reset_zdd()

        return self._zdd

    @property
    def solutions(self):
        """
        Returns a generator for each solution stored in the zdd
        """
        for x in iter(self.zdd):
            sol = list(set(chain(*x)))
            if self._row_labels is not None:
                sol = [self._row_labels[row] for row in sol]
            yield sol

    def _reset_zdd(self):
        n = self.matrix.A.shape[0]
        universe = list(combinations(range(n), 2))
        GraphSet.set_universe(universe)
        self._zdd = GraphSet()

    def _choose_column(self):
        S = np.inf
        for j in self.matrix.h.sweep('R'):
            if j.S < S:
                col = j
                S = j.S

        return col

    def search(self, k=0, partials=None, level=0):
        if level == 0:
            self._reset_zdd()

        if partials is None:
            partials = deque()

        if self.matrix.h.R == self.matrix.h:
            if len(partials) == 0:
                print("Your matrix is empty!")
            else:
                sol = list(partials)
                self.zdd.add(list(zip(sol[:-1], sol[1:])))
            return

        c = self._choose_column()
        self.matrix.cover(c)
        for r in c.sweep('D'):
            Ok = r
            partials.append(r.row)  # r is included in partial solution
            for j in r.sweep('R'):
                self.matrix.cover(j.column)
            self.search(k+1, partials, level+1)
            r = Ok
            c = r.column
            for j in r.sweep('L'):
                self.matrix.uncover(j.column)

            if len(partials) > 0:
                partials.pop()
        self.matrix.uncover(c)

        return

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