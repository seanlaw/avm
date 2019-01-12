#!/usr/bin/env python

from matrix import MATRIX
import numpy as np
from scipy.sparse import csc_matrix
from collections import deque
from itertools import permutations

class DLX(object):
    def __init__(self, A, column_labels=None, primary_idx=None):
        self._A = A
        self._column_labels = column_labels
        self._primary_idx = primary_idx
        self._matrix = None

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

    def _choose_column(self):
        S = np.inf
        for j in self.matrix.h.sweep('R'):
            if j.S < S:
                col = j
                S = j.S

        return col

    def search(self, k=0, partials=None, solutions=None):
        if partials is None:
            partials = deque()

        if solutions is None:
            solutions = []

        if self.matrix.h.R == self.matrix.h:
            if len(partials) == 0:
                print("Your matrix is empty!")
            else:
                solutions.append(list(partials))
            return

        c = self._choose_column()
        self.matrix.cover(c)
        for r in c.sweep('D'):
            Ok = r
            partials.append(r.row)  # r is included in partial solution
            for j in r.sweep('R'):
                self.matrix.cover(j.column)
            self.search(k+1, partials, solutions)
            r = Ok
            c = r.column
            for j in r.sweep('L'):
                self.matrix.uncover(j.column)

            if len(partials) > 0:
                partials.pop()
        self.matrix.uncover(c)

        if self._column_labels is not None:
            solutions = [self._column_labels[row] for soln in solutions
                         for row in soln]

        return solutions

if __name__ == "__main__":
    # Knuth Example
    arr = np.array([[0, 0, 1, 0, 1, 1, 0],
                    [1, 0, 0, 1, 0, 0, 1],
                    [0, 1, 1, 0, 0, 1, 0],
                    [1, 0, 0, 1, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 1, 0, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)

    dlx = DLX(csc)
    print(dlx.search())

    # Wikipedia Example
    arr = np.array([[1, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1],
                    [0, 0, 1, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1],
                    [0, 1, 0, 0, 0, 0, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)
    col_labels = {0: 'A',
                  1: 'B',
                  2: 'C',
                  3: 'D',
                  4: 'E',
                  5: 'F',
                 }

    dlx = DLX(csc, col_labels)
    print(dlx.search())

    # Generalized Exact Cover Example
    # 2x2 grid with one L-shaped and two Singleton-shaped pieces.
    #                0  1  2  3  A  B  C
    arr = np.array([[1, 0, 1, 1, 1, 0, 0],
                    [1, 0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 0, 1, 0],
                    [0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 0, 1, 0, 1, 0],
                    [1, 0, 0, 0, 0, 0, 1],
                    [0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 1, 0, 0, 0, 1],
                    [0, 0, 0, 1, 0, 0, 1],
                   ], dtype='u1')

    csc = csc_matrix(arr)
    
    # Permute all combinations of pieces
    pieces = {4: 'A', 5: 'B', 6: 'C'}
    for i in range(1, len(pieces)+1):
        for perm in permutations(pieces.keys(), i):
            dlx = DLX(csc, primary_idx=list(perm))
            print(f"Pieces {[pieces[p] for p in perm]}:", dlx.search())

