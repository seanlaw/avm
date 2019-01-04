#!/usr/bin/env python

import game
import piece

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_positions()
    print(g.pieces_pos)