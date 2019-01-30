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

    dxz = DXZ(csc)
    #dxz.search(log_time=True, log_resources=True, every=60.0)
    dxz.search(log_time=True, log_resources=False)
    logger.warning(len(dxz))
    #dxz.print_solutions()
