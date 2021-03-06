#!/usr/bin/env python

import game
from dxz import DXZ
from scipy.sparse import csc_matrix
import logging

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_positions()
    csc = csc_matrix(g.pieces_pos, dtype='u1')

    start = g.m * g.n + 1
    stop = g.pieces_pos.shape[1]

    primary_idx = list(range(start, stop))
    dxz = DXZ(csc, primary_idx=primary_idx)
    #dxz.search(log_time=True, log_resources=True, every=60.0)
    dxz.search(log_time=True, log_resources=False)
    logger.warning(len(dxz.zdd))

    dxz.dump()
    dxz = DXZ(csc, primary_idx=primary_idx)
    dxz.load()
    logger.warning(len(dxz.zdd))
    #for sol in dxz.solutions:
    #    print(g.pieces_pos[sol, :])
    #dxz.print_solutions()
