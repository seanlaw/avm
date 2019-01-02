#!/usr/bin/env python

import game
import piece

if __name__ == '__main__':
    g = game.GAME()
    print(g.board)
    g.enumerate_states()
