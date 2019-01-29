#!/usr/bin/env python

from matrix import MATRIX
import numpy as np
from scipy.sparse import csc_matrix
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
        self._zdd = None

    @property
    def A(self):
        return self._A

    @property
    def primary_idx(self):
        return self._primary_idx

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
            vertices.append(-1)  # Terminal zdd Truth node
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
    def solutions(self):
        """
        Returns a generator for each solution stored in the zdd
        """
        for x in iter(self.zdd):
            sol = set(chain(*x))
            sol.remove(-1)  # Remove terminal zdd Truth node
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

    def _search(self, level=0):
        """
        """
        if self.matrix.h.R == self.matrix.h:
            # Empty matrix
            return True

        c = self._choose_column()
        x = GraphSet() 
        self.matrix.cover(c)
        for r in c.sweep('D'):
            for j in r.sweep('R'):
                self.matrix.cover(j.column)
            y = self._search(level+1)
            if not y is False:
                x = x.union(self._unique(r, y))

            for j in r.sweep('L'):
                self.matrix.uncover(j.column)

        self.matrix.uncover(c)

        return x

    def _unique(self, r, y):
        if y is True:
            return GraphSet([[(r.row, -1)]])
        elif isinstance(y, GraphSet):
            return GraphSet([[(r.row, -1)]]).join(y)
        else:
            # We should never be in here
            return

    def search(self):
        self.zdd.clear()  # Initializes GraphSet
        self.zdd = self._search()

    def print_solutions(self):
        for sol in self.solutions:
            print(sol)
        print()

if __name__ == "__main__":
    # Simple Example
    arr = np.array([[0, 1, 0],
                    [0, 0, 1],
                    [1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 1],
                    [1, 1, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)
    
    dxz = DXZ(csc)
    dxz.search()
    dxz.print_solutions()

    #dxz = DXZ(csc, primary_idx=[1,2])
    #dxz.search()
    #dxz.print_solutions()   

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
    dxz.print_solutions()

    # Knuth Example
    arr = np.array([[0, 0, 1, 0, 1, 1, 0],
                    [1, 0, 0, 1, 0, 0, 1],
                    [0, 1, 1, 0, 0, 1, 0],
                    [1, 0, 0, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 1, 0, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)

    dxz = DXZ(csc)
    dxz.search()
    dxz.print_solutions()  

    # Wikipedia Example
    arr = np.array([[1, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1],
                    [0, 0, 1, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1],
                    [0, 1, 0, 0, 0, 0, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)
    row_labels = {0: 'A',
                  1: 'B',
                  2: 'C',
                  3: 'D',
                  4: 'E',
                  5: 'F',
                 }

    dxz = DXZ(csc, row_labels)
    dxz.search()
    dxz.print_solutions()

    # Generalized Exact Cover Example
    # 2x2 grid with one L-shaped and two Singleton-shaped pieces.
    #                0  1  2  3  A  B  C
    arr = np.array([[1, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0],  # No cover, row 1
                    [1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 0, 1, 0, 1, 0],
                    [0, 0, 0, 0, 0, 1, 0],  # No cover, row 6
                    [1, 0, 0, 0, 0, 0, 1],
                    [0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 1, 0, 0, 0, 1],
                    [0, 0, 0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1],  # No cover, row 11
                   ], dtype='u1')

    csc = csc_matrix(arr)
    
    pieces = {4: 'A', 5: 'B', 6: 'C'}
    dxz = DXZ(csc, primary_idx=pieces.keys())
    dxz.search()
    dxz.print_solutions()

    # Generalized Cover Example #2
    # 3x3 grid with one L-shaped, one (2x2) Square-shaped, and one 
    # Singleton-shaped piece.
    # Columns 0-8 (inclusive) represent the board and are secondary.
    # The L-shaped ('A') piece is primary (i.e., required) while the 
    # Square-shaped ('B')and Singleton-shaped ('C') pieces are secondary.
    #                0  1  2  3  4  5  6  7  8  A  B  C
    arr = np.array([[1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0],
                    [0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],  # No cover, row 4                    
                    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
                    [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],  # No cover, row 9                 
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # No cover, row 19                 
                   ], dtype='u1')

    csc = csc_matrix(arr)

    pieces = {9: 'A', 10: 'B', 11: 'C'}
    dxz = DXZ(csc, primary_idx=pieces.keys())
    dxz.search()
    dxz.print_solutions()