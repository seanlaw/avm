#!/usr/bin/env python

import numpy as np
import piece
from scipy.ndimage.interpolation import shift

class GAME(object):
    def __init__(self, n=5, m=5):
        if m >= 3:
            self._m = m

        if n >= 3:
            self._n = n

        self._board = None
        self._new_board_flag = True

        self._tmp_board = None
        self._new_tmp_board_flag = True

        self._pieces = {
            'red': piece.RED(),
            'orange': piece.ORANGE(),
            'yellow': piece.YELLOW(),
            'green': piece.GREEN(),
            'blue': piece.BLUE(),
            'purple': piece.PURPLE(),
            'white_1': piece.WHITE(),
            'white_2': piece.WHITE(),
            'white_3': piece.WHITE(),
        }

    @property
    def m(self):
        return self._m

    @m.setter
    def m(self, value):
        self.new_board_flag = True
        self._new_tmp_board_flag = True
        self._m = value
    
    @property
    def n(self):
        return self._n

    @n.setter
    def n(self, value):
        self.new_board_flag = True
        self._new_tmp_board_flag = True
        self._n = value

    @property
    def pieces(self):
        return self._pieces

    @property
    def red(self):
        return self._pieces['red']

    @property
    def orange(self):
        return self._pieces['orange']

    @property
    def yellow(self):
        return self._pieces['yellow']

    @property
    def green(self):
        return self._pieces['green']

    @property
    def blue(self):
        return self._pieces['blue']

    @property
    def purple(self):
        return self._pieces['purple']

    @property
    def white_1(self):
        return self._pieces['white_1']

    @property
    def white_2(self):
        return self._pieces['white_2']

    @property
    def white_3(self):
        return self._pieces['white_3']

    @property
    def new_board_flag(self):
        return self._new_board_flag

    @new_board_flag.setter
    def new_board_flag(self, value):
        """
        Set boolean flag for whether or not a new board should be 
        created when accessing the self.board attribute
        """
        self._new_board_flag = value

    @property
    def new_tmp_board_flag(self):
        return self._new_tmp_board_flag

    @new_tmp_board_flag.setter
    def new_tmp_board_flag(self, value):
        """
        Set boolean flag for whether or not a new tmp board should be 
        created when accessing the self.tmp_board attribute
        """
        self._new_tmp_board_flag = value

    @property
    def board(self):
        if self.new_board_flag:
            self.new_board_flag = False
            # Add an extra column to account for the exit space region
            self._board = np.zeros((self.n, self.m+1), dtype='u1')
            self._block_exit_column('board', self.exit_col_idx)

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

    @property
    def tmp_board(self):
        if self.new_tmp_board_flag:
            self.new_tmp_board_flag = False
            # Add an extra column to account for the exit space region
            self._tmp_board = np.zeros((self.n, self.m+1), dtype='u1')
            
        return self._tmp_board

    @tmp_board.setter
    def tmp_board(self, value):
        try:
            val, indices = value
        except:
            if value is None:
                self._tmp_board = None
            else:
                self._tmp_board.fill(int(value))
        else:
            self._tmp_board[indices] = int(val)

    @property
    def exit_col_idx(self):
        return np.s_[1:self.n, self.m]

    def _block_exit_column(self, board_name, idx, value=2):
        """
        """
        setattr(self, board_name, (value, idx))

    def _reset_board(self, board_name, value=0, block_idx=None, block_value=2):
        """
        """
        setattr(self, board_name, value)
        if block_idx is not None:
            self._block_exit_column(board_name, block_idx, block_value)

    def enumerate_states(self):
        getattr(self, 'tmp_board')
        for k in self.pieces.keys():
            for row in range(self.n):
                self._reset_board('tmp_board')
                self.tmp_board = (1, tuple(self.pieces[k].ref_idx.T))
                shift(self.tmp_board, (row, 0), output=self.tmp_board)
                for col in range(self.m):
                    if col == 0:
                        print(self.tmp_board)
                    else:
                        shift(self.tmp_board, (0, 1), output=self.tmp_board)
                        print(self.tmp_board)

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

if __name__ == '__main__':
    game = GAME()