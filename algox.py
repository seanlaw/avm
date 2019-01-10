#!/usr/bin/env python

import numpy as np
from scipy.sparse import csc_matrix
from collections import deque
from dlx import DLX

def _search(x, ref_rows, partials=None, solutions=None, level=0):
    """
    """
    if partials is None:
        partials = deque()

    if solutions is None:
        solutions = []

    rows = np.array(range(x.shape[0]))
    cols = np.array(range(x.shape[1]))

    if len(cols) == 0:
        if len(partials) == 0:
            print("Your matrix is empty!")
        else:
            solutions.append(list(partials))
        return
    
    col_sum = np.sum(x, axis=0)
    c = np.argmin(col_sum)
    if np.min(col_sum) == 0:  # no solution
        if len(partials) > 0:
            partials.pop()
        return

    for r in x[:, c].nonzero()[0]:
    
        partials.append(ref_rows[r])  # r is included in partial solution
        delete_cols = x[r, :].nonzero()[1]
        delete_rows = np.unique(x[:, delete_cols].nonzero()[0])
        keep_rows = np.delete(rows, delete_rows)
        keep_cols = np.delete(cols, delete_cols)
        
        new_ref_rows = dict(list(enumerate([ref_rows[k] for k in keep_rows])))
        
        _search(x[keep_rows][:, keep_cols], 
               new_ref_rows, 
               partials, 
               solutions,
               level=level+1,
              )
        
        if len(partials) > 0:
            partials.pop()
    
    return solutions

def search(x, y, primary_idx=None):
    """
    Dancing Links Wrapper
    """

    return 

if __name__ == '__main__':
    # cols=['a','b','c','d']
    # lines=[['a'],['b'],['c'],['d'],
    #     ['a','b'],['a','c'],['a','d'],['b','c'],
    #     ['b','d'],['c','d'],['a','b','c'],['a','b','d'],
    #     ['a','c','d'],['b','c','d'],['a','b','c','d'],]

    arr = np.array([[1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                    [1, 1, 0, 0],
                    [1, 0, 1, 0],
                    [1, 0, 0, 1],
                    [0, 1, 1, 0],
                    [0, 1, 0, 1],
                    [0, 0, 1, 1],
                    [1, 1, 1, 0],
                    [1, 1, 0, 1],
                    [1, 0, 1, 1],
                    [0, 1, 1, 1],
                    [1, 1, 1, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)

    ref_rows = dict(list(enumerate(range(csc.shape[0]))))
    #print(search(csc, ref_rows))

    # Exact Cover Example #1
    arr = np.array([[1, 0, 0, 0],
                    [0, 1, 1, 0],
                    [1, 0, 0, 1],
                    [0, 0, 1, 1],
                    [0, 1, 0, 0],
                    [0, 0, 1, 0]
                   ], dtype='u1')

    csc = csc_matrix(arr)
    ref_rows = dict(list(enumerate(range(csc.shape[0]))))

    print(_search(csc, ref_rows))
    print(search(csc, ref_rows))

    # Exact Cover Example #2
    arr = np.array([[1, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 1, 1, 0, 1],
                    [0, 0, 1, 0, 1, 1, 0],
                    [0, 1, 1, 0, 0, 1, 1],
                    [0, 1, 0, 0, 0, 0, 1]
                   ], dtype='u1')

    csc = csc_matrix(arr)
    ref_rows = {0: 'A',
                1: 'B',
                2: 'C',
                3: 'D',
                4: 'E',
                5: 'F',
               }

    #print(_search(csc, ref_rows))
    #print(search(csc, ref_rows))

    # Generalized Cover Example #1
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
    ref_rows = dict(list(enumerate(range(csc.shape[0]))))

    #print(search(csc, ref_rows, primary_idx=[0,2,3]))
    #print(search(csc, ref_rows, primary_idx=[0,1,2,3]))
    #print(search(csc, ref_rows, primary_idx=[0]))

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
                    [1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0],
                    [0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0],
                    [0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                   ], dtype='u1')

    csc = csc_matrix(arr)
    ref_rows = dict(list(enumerate(range(csc.shape[0]))))

    #print(search(csc, ref_rows, primary_idx=[9]))