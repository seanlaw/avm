#!/usr/bin/env python

from matrix import MATRIX
import numpy as np
from scipy.sparse import csc_matrix
from fastcache import lru_cache
from bitarray import bitarray
from graphillion import GraphSet
from itertools import combinations, chain
import time
import logging
import threading
import os
import psutil
import pickle

logger = logging.getLogger(__name__)

class DXZ(object):
    def __init__(self, A, row_labels=None, primary_idx=None):
        self._A = A
        self._row_labels = row_labels
        self._primary_idx = primary_idx
        self._matrix = None
        self._universe = None
        self._zdd = None
        self._bitarray = None
        self._pid = os.getpid()
        self._search_incomplete = False 

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
    def bitarray(self):
        if self._bitarray is None:
            n = self._matrix.A.shape[0]
            m = self._matrix.A.shape[1]
            self._bitarray = bitarray(n*m, endian='little')
            self._bitarray.setall(0)

        return self._bitarray

    @property
    def pid(self):
        return self._pid

    @property
    def search_incomplete(self):
        return self._search_incomplete

    @search_incomplete.setter
    def search_incomplete(self, value):
        self._search_incomplete = value

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
    
    def memo_cache(self):
        c = self._choose_column()
        x = GraphSet() 
        self.matrix.cover(c)
        for r in c.sweep('D'):
            self.bitarray[r.row*self.A.shape[1] + c.N] = 1

        for r in c.sweep('D'):
            for j in r.sweep('R'):
                self.matrix.cover(j.column)
                self.bitarray[r.row * self.A.shape[1] + j.column.N] = 1
            int_key = int.from_bytes(self.bitarray.tobytes(), 'little')
            y = self._search(int_key)
            if not y is False:
                x = x.union(self._unique(r, y))

            for j in r.sweep('L'):
                self.matrix.uncover(j.column)
                self.bitarray[r.row * self.A.shape[1] + j.column.N] = 0

        self.matrix.uncover(c)

        return x

    @lru_cache(maxsize=None)
    def _search(self, int_key):
        """
        """
        if self.matrix.h.R == self.matrix.h:
            # Empty matrix
            return True

        x = self.memo_cache()

        return x

    def _unique(self, r, y):
        if y is True:
            return GraphSet([[(r.row, -1)]])
        elif isinstance(y, GraphSet):
            return GraphSet([[(r.row, -1)]]).join(y)
        else:
            # We should never be in here
            return

    def search(self, log_time=False, log_resources=False, every=60.0):
        """
        This is a convenient wrapper function around the `_search` function
        """

        self.search_incomplete = True

        # Logging time
        start_time = time.time()
        if log_resources:
            self._log_resources(start_time, every)

        # The real work is done here
        self.zdd.clear()  # Initializes GraphSet

        self.bitarray.setall(1)
        int_key = int.from_bytes(self.bitarray.tobytes(), 'little')
        self.zdd = self._search(int_key)
        self.search_incomplete = False

        if log_time:
            msg = (self._get_human_readable_time(time.time() - start_time))
            logger.warning(msg)
            logger.warning(self._search.cache_info())
            logger.warning(len(self.zdd))

    def _log_resources(self, start_time, every=60.0):
        if self.search_incomplete:
            # Adjust for time drift/creep
            adjusted_every = every - ((time.time()-start_time) % every)
            threading.Timer(adjusted_every, self._log_resources, [start_time, every]).start()

            elapsed_time = self._get_human_readable_time(time.time() - start_time)
            process = psutil.Process(self._pid)
            memory = process.memory_info()[0] / (1024.0 ** 3)
            percent = process.memory_percent()

            msg = f"{elapsed_time} {memory} GB {percent} % {self._search.cache_info()} {len(self.zdd)}"
            logger.warning(msg)

    def _get_human_readable_time(self, total_time):
        hours, rem = divmod(total_time, 3600)
        minutes, seconds = divmod(rem, 60)
        hours = int(hours)
        minutes = int(minutes)

        return f"{hours:0>2}:{minutes:0>2}:{seconds:05.2f}"

    def print_solutions(self):
        for sol in self.solutions:
            print(sol)
        print()

    def dump(self, fzdd='zdd.dxz', funiverse='universe.dxz'):
        with open(fzdd, 'wb') as fp:
            self.zdd.dump(fp)

        with open(funiverse, 'wb') as fp:
            pickle.dump(GraphSet.universe(), fp)
        

    def save(self, fzdd='zdd.dxz', funiverse='universe.dxz'):
        """
        Convenience function that calls `dump` function internally
        """
        self.dump(fzdd, funiverse)

    def load(self, fzdd='zdd.dxz', funiverse='universe.dxz'):
        """
        """
        with open(funiverse, 'rb') as fp:
            GraphSet.set_universe(pickle.load(fp), traversal='as-is')

        with open(fzdd, 'rb') as fp:
            self.zdd = GraphSet.load(fp)

if __name__ == "__main__":
    arr = np.array([[0, 0, 0, 1, 0],
                    [1, 1, 0, 1, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1],
                    [0, 1, 0, 0, 1],
                    [0, 0, 1, 0, 1]], dtype='u1')

    csc = csc_matrix(arr)

    dxz = DXZ(csc, primary_idx=[3,4])
    dxz.search(log_time=True, log_resources=False)
    dxz.print_solutions()
    #exit()

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
    dxz.search(log_time=True, log_resources=False)
    dxz.print_solutions()
    #exit()
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
    dxz.search(log_time=True, log_resources=False)
    dxz.print_solutions()
