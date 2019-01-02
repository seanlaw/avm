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
            self._board = np.zeros((self.n, self.m+1), dtype='u1')
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
                self._board.fill(int(value))
        else: 
            self._board[indices] = int(val)

    def _block_exit_column(self, value=1):
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
    def __init__(self, ref_idx=None, name=None, shape=None):
        self._ref_idx = ref_idx
        self._name = name
        self._shape = shape

    @property
    def ref_idx(self):
        return self._ref_idx

    @ref_idx.setter
    def ref_idxx(self, value):
        self._ref_idx = value

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape

class RED(PIECE):
    def __init__(self):
        shape = "o-o"
        ref_idx = np.array([[0,0], [0,1]])
        super().__init__(ref_idx=ref_idx, name='A', shape=shape)

class ORANGE(PIECE):
    def __init__(self):
        shape = """\
          o  
         / \ 
        o   o
        """
        ref_idx = np.array([[1,0], [0,1], [1,2]])
        super().__init__(ref_idx=ref_idx, name='F', shape=shape)

class YELLOW(PIECE):
    shape = """\
    o
     \ 
      o
    """
    ref_idx = np.array([[0,0], [1,1]])
    def __init__(self):
        super().__init__(ref_idx=ref_idx, name='B', shape=shape)

class GREEN(PIECE):
    def __init__(self):
        shape = """\
        o-o
           \ 
            o
        """
        ref_idx = np.array([[0,0], [0,1], [1,2]])
        super().__init__(ref_idx=ref_idx, name='C', shape=shape)

class BLUE(PIECE):
    def __init__(self):
        shape = """\
          o
          |
        o-o
        """
        ref_idx = np.array([[0,1], [1,0], [1,1]])
        super().__init__(ref_idx=ref_idx, name='D', shape=shape)

class PURPLE(PIECE):
    def __init__(self):
        shape = """\
          o
         / \ 
        o   o
        """
        ref_idx = np.array([[0,1], [1,0], [1,2]])
        super().__init__(ref_idx=ref_idx, name='E', shape=shape)

class WHITE(PIECE):
    def __init__(self):
        shape = "o"
        ref_idx = np.array([[0,0]])
        uper().__init__(ref_idx=ref_idx, name='E', shape=shape)

if __name__ == '__main__':
    red = RED()
    print(red.ref_idx)
    #orange = ORANGE()
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
