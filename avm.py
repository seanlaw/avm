#!/usr/bin/env python

import scipy.sparse
import numpy as np

class GAME(object):
    def __init__(self, n=5, m=5):
        self._m = m
        self._n = n
        self._board = None
        self._new_board = True

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        self._new_board = True
        self._m = value
    
    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self._new_board = True
        self._n = value

    @property
    def new_board(self):
        return self._new_board

    @new_board.setter
    def new_board(self, value):
        """
        Set boolean flag for whether or not
        a new board should be created when
        accessing the self.board attribute
        """
        self._new_board = value

    @property
    def board(self):
        if self.new_board:
            # Add an extra column to account
            # for the exit space
            self._board = np.zeros((self.n, self.m+1), dtype=bool)
            self._block_exit_column()
            self.new_board = False
            
        return self._board

    @board.setter
    def board(self, value):
        try:
            val, indices = value
        except:
            if value is None:
                self._board = None
            else:
                self._board.fill(value)
        else: 
            self._board[indices] = val

    def _block_exit_column(self, value=True):
        indices = np.s_[1:self.n, self.m]
        self.board = (value, indices)

    def reset_board(self):
        self.board = False
        self._block_exit_column()

    def _piece_fits(self, piece):
        """
        Checks if piece can be placed on grid in the 
        specified position without overlapping with
        other existing pieces.
        """
        
        # Some logic for finding a clash

        return True

    def add_piece(self, piece):
        self.piece_fits(piece)

    def del_piece(self, piece):
        #self
        pass

class PIECE(object):
    def __init__(self, x=None, y=None, name=None, shape=None):
        self._x = x
        self._y = y
        self._name = name
        self._shape = shape

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def pos(self):
        return (self._x, self.y)

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape

class RED(PIECE):
    def __init__(self, x=None, y=None):
        shape = "o-o"
        super().__init__(x, y, name='A', shape=shape)

class ORANGE(PIECE):
    def __init__(self, x=None, y=None):
        shape = """\
          o  
         / \ 
        o   o
        """
        super().__init__(x, y, name='F', shape=shape)

class YELLOW(PIECE):
    shape = """\
    o
     \ 
      o
    """
    def __init__(self, x=None, y=None):
        super().__init__(x, y, name='B', shape=shape)

class GREEN(PIECE):
    def __init__(self, x=None, y=None):
        shape = """\
        o-o
           \ 
            o
        """
        super().__init__(x, y, name='C', shape=shape)

class BLUE(PIECE):
    def __init__(self, x=None, y=None):
        shape = """\
          o
          |
        o-o
        """
        super().__init__(x, y, name='D')

class PURPLE(PIECE):
    def __init__(self, x=None, y=None):
        shape = """\
          o
         / \ 
        o   o
        """
        super().__init__(x, y, name='E', shape=shape)

class WHITE(PIECE):
    def __init__(self):
        shape = "o"
        uper().__init__(x, y, name='E', shape=shape)

if __name__ == '__main__':
    #red = RED(0, 0)
    #print(red.pos, red.shape)
    #orange = ORANGE(0,0)
    #print(orange.shape)
    game = GAME()
    print(game.board)
    game.board = True
    print(game.board)
    game.reset_board()
    print(game.board)
    game.m = 2
    print(game.board)
    game.n = 2
    print(game.board)
