#!/usr/bin/env python

import game
import piece

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_pieces()
    print(g.pieces_pos, g.pieces_name)