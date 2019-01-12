#!/usr/bin/env python

import game
import piece
from itertools import combinations
from dlx import DLX
from scipy.sparse import csc_matrix

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_positions()
    print(g.pieces_pos[:20])
    csc = csc_matrix(g.pieces_pos, dtype='u1')
    start = (g.n + 1) * (g.m + 1)
    stop = start + len(g.pieces.keys())
    pieces = dict(zip(range(start, stop), g.pieces.keys()))

    # TODO
    # 1. Always include red piece
    # 1. Always use 3 or more pieces

    for i in range(1, len(pieces)+1):
        for combo in combinations(pieces.keys(), i):
            dlx = DLX(csc, primary_idx=list(combo))
            print(f"Pieces {[pieces[c] for c in combo]}:", dlx.search())