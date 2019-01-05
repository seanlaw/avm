#!/usr/bin/env python

import numpy as np
from scipy.sparse import csc_matrix
from collections import deque

def search(x, ref_rows, partials=None, solutions=None, primary_idx=None):
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
    if np.min(col_sum) == 0:  # no solution
        partials.pop()
        return

    c = np.argmin(col_sum)
    for r in x[:, c].nonzero()[0]:

        partials.append(ref_rows[r])  # r is included in partial solution
        delete_cols = x[r, :].nonzero()[1]
        delete_rows = np.unique(x[:, delete_cols].nonzero()[0])        
        keep_rows = np.delete(rows, delete_rows)
        keep_cols = np.delete(cols, delete_cols)
        
        new_ref_rows = dict(list(enumerate([ref_rows[k] for k in keep_rows])))
        
        search(x[keep_rows][:, keep_cols], new_ref_rows, partials, solutions)
        
        if len(partials) > 0:
            partials.pop()
    
    return solutions

if __name__ == '__main__':

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

    print(search(csc, ref_rows))

    # Generalized Cover Example #1