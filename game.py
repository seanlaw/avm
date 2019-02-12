#!/usr/bin/env python

import numpy as np
import piece
from scipy.ndimage.interpolation import shift
from scipy.sparse import coo_matrix

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

        self._pieces_pos = None

        self._piece_to_one_hot = None
        self._one_hot_to_piece = None

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
    def pieces_pos(self):
        return self._pieces_pos

    @pieces_pos.setter
    def pieces_pos(self, value):
        self._pieces_pos = value

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
            self._board = np.zeros((self.n+1, self.m+1), dtype='u1')
            self._block_exclusion_zone('board', self.exclusion_idx)

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
            self._tmp_board = np.zeros((self.n+1, self.m+1), dtype='u1')
            
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
    def exclusion_idx(self):
        """
        Generate indices for the exclusion zone.

        This is denoted by `1` for `n = 5` and `m = 5`

        0 0 0 0 0 0
        0 0 0 0 0 1
        0 0 0 0 0 1
        0 0 0 0 0 1
        0 0 0 0 0 1
        1 1 1 1 1 1

        Note that the grid is 6 x 6 since we need to account
        for the exit space.
        """
        row_idx = []
        col_idx = []
        for row in range(1, self.n+1):
            if row < self.n:
                row_idx.append(row)
                col_idx.append(self.m)
            else:
                for col in range(self.m+1):
                    row_idx.append(row)
                    col_idx.append(col)

        return tuple([row_idx, col_idx])

    def _block_exclusion_zone(self, board_name, idx, value=2):
        """
        See `exclusion_idx` for exclusion zone
        """
        setattr(self, board_name, (value, idx))

    def _reset_board(self, board_name, value=0, block_idx=None, block_value=2):
        """
        """
        setattr(self, board_name, value)
        if block_idx is not None:
            self._block_exclusion_zone(board_name, block_idx, block_value)

    def piece_to_one_hot(self, piece_key, reset=False):
        if self._piece_to_one_hot is None or reset:
            self._piece_to_one_hot = {}
            keys = self.pieces.keys()

            for i, k in enumerate(keys):
                self._piece_to_one_hot[k] = [0] * len(keys)
                self._piece_to_one_hot[k][i] = 1

            # key=None maps to no piece (i.e., all zeros)
            self._piece_to_one_hot[None] = [0] * len(keys)

        return self._piece_to_one_hot[piece_key]

    def one_hot_to_piece(self, idx, reset=False):
        if self._one_hot_to_piece is None or reset:
            keys = self.pieces.keys()
            self._one_hot_to_piece = [None] * len(keys)

            for i, k in enumerate(keys):
                self._one_hot_to_piece[i] = k

        return self._one_hot_to_piece[idx]

    def enumerate_positions(self):
        """
        For each piece orientation (designated by ref_idx):
        1. Clear the tmp_board (fill with zeros)
        2. Place the reference piece on the upper left of the tmp board
        3. Shift the piece down & across to the correct row & col, 
           respectively
        4. Store the piece position in a flattened dense matrix if the 
           positioned piece does not land inside of the exclusion zone and
           also append the one hot encoded piece name to this flattened. There 
           are situations where a part of piece may be off of the board but 
           not inside of the exclusion zone. In these cases, we also check 
           that the entire piece is still on the board.

        Since the number of enumerated states is small, we use a dense matrix.
        The final dimensions of the dense matrix is:

            n * m + 1 exit space + n_pieces

        and, therefore, includes the exclusion zone and one hot encoded piece 
        name. A dense matrix makes it easier to manipulate individual matrix 
        elements, rows, and columns. 

        Stores dense position matrix in `pieces_pos` attribute
        """

        getattr(self, 'tmp_board')

        pieces_pos_list = []

        n_pos = 0
        n = self.n
        m = self.m

        for k in self.pieces.keys():
            # Add edge case when the piece is NOT on the board
            self._reset_board('tmp_board')
            flat_board = self.tmp_board[:n, :m].flatten()
            board_list = flat_board.tolist()
            board_list.append(self.tmp_board[0, m])
            board_list.extend(self.piece_to_one_hot(k))
            pieces_pos_list.append(board_list)
            n_pos += 1
            piece_n_pos = 1

            for ref_idx in self.pieces[k].ref_idx:
                # Add all other permutations
                n_ones_on_board = len(ref_idx)
                for row in range(self.n):
                    for col in range(self.m):
                        self._reset_board('tmp_board')
                        self.tmp_board = (1, tuple(ref_idx.T))
                        shift(self.tmp_board, (row, col), 
                              output=self.tmp_board)

                        if not np.any(self.tmp_board[self.exclusion_idx]) and \
                           self.tmp_board.sum() == n_ones_on_board:
                            flat_board = self.tmp_board[:n, :m].flatten()
                            board_list = flat_board.tolist()
                            board_list.append(self.tmp_board[0, m])
                            board_list.extend(self.piece_to_one_hot(k))
                            pieces_pos_list.append(board_list)
                            n_pos += 1
                            piece_n_pos += 1

        self.pieces_pos = np.array(pieces_pos_list, dtype='u1')

if __name__ == '__main__':
    game = GAME()
    game.enumerate_positions()
    print(game.pieces_pos.shape)
