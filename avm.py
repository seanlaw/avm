#!/usr/bin/env python

import game
import piece

if __name__ == '__main__':
    g = game.GAME()
    g.enumerate_states()
    print(g.states.todense())