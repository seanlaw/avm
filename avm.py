#!/usr/bin/env python

import game
import piece
from itertools import combinations
from dlx import DLX
from dxz import DXZ
from scipy.sparse import csc_matrix

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_positions()

    for i in g.pieces_pos:
        print(i)

    csc = csc_matrix(g.pieces_pos, dtype='u1')
    start = (g.n * g.m + 1)
    stop = start + len(g.pieces.keys())
    pieces = dict(zip(range(start, stop), g.pieces.keys()))

    #list(pieces.keys())

    dxz = DXZ(csc)
    dxz.search()
    dxz.print_solutions()