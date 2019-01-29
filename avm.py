#!/usr/bin/env python

import game
from dxz import DXZ
from scipy.sparse import csc_matrix

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_positions()

    csc = csc_matrix(g.pieces_pos, dtype='u1')

    dxz = DXZ(csc)
    dxz.search(log_time=True)
    #dxz.print_solutions()
