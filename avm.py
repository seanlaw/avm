#!/usr/bin/env python

import game
import piece
from itertools import combinations
from dlx import DLX
from scipy.sparse import csc_matrix

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_positions()
    # 22 x 51 x 34 x 51 x 66 x 51 x 26 x 26 x 26 = 115,100,207,247,168
    # Upper bound with overlap is 115 Trillion (14 zeros)
    csc = csc_matrix(g.pieces_pos, dtype='u1')
    start = (g.n * g.m + 1)
    stop = start + len(g.pieces.keys())
    pieces = dict(zip(range(start, stop), g.pieces.keys()))

    dlx = DLX(csc, primary_idx=list(pieces.keys()))
    dlx.search()