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

    csc = csc_matrix(g.pieces_pos, dtype='u1')
    start = (g.n * g.m + 1)
    stop = start + len(g.pieces.keys())
    pieces = dict(zip(range(start, stop), g.pieces.keys()))

    #dlx = DLX(csc, primary_idx=list(pieces.keys()))
    #dlx.search()
    dxz = DXZ(csc, primary_idx=list(pieces.keys()))
    dxz.search()