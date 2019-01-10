from node import ROOT, DATA, COLUMN
import numpy as np

class MATRIX(object):
    def __init__(self, A, column_labels=None, secondary_idx=None):
        self._h = ROOT()  # Master "root" header for all headers
        self._column_headers = {}
        self._A = A.sorted_indices()
        self._populate_matrix()
        self._column_labels = column_labels
        self._secondary_idx = secondary_idx

    @property
    def h(self):
        return self._h

    @property
    def column_headers(self):
        return self._column_headers

    @property
    def A(self):
        return self._A

    @property
    def secondary_idx(self):
        return self._secondary_idx

    def _populate_matrix(self):
        """
        """

        self._add_column_headers()
        self._add_data()

    def _add_column_headers(self):
        """
        Add column headers to root node, `h`
        """

        for col in range(self.A.shape[1]):
            self.h.L.R = COLUMN()
            self.h.L.R.L = self.h.L
            self.h.L.R.R = self.h
            self.h.L = self.h.L.R
            self.h.L.N = col
            self.h.L.S = self.A[:, col].nonzero()[0].shape[0]
            self.column_headers[col] = self.h.L

    def _add_data(self):
        """
        Add data to column headers
        """

        for row in range(self._A.shape[0]):
            last = False
            for col in self._A[row, :].nonzero()[1]:
                x = DATA()
                col_header = self.column_headers[col]
                
                # Add new node to bottom of column
                x.U = col_header.U
                x.D = col_header
                x.D.U = x
                x.U.D = x
                x.column = col_header
                x.row = row

                if last:
                    x.L = last
                    x.R = last.R
                    x.L.R = x
                    x.R.L = x
                last = x

        # Left/Right Indices
        for row in range(self._A.shape[0]):
            left_idx = np.roll(self._A[row, :].nonzero()[1], 1)
            right_idx = np.roll(self._A[row, :].nonzero()[1], -1)                
            #print(row, left_idx)
            #print(row, right_idx)

        # Up/Down Indices
        for col in range(self._A.shape[1]):
            up_idx = np.roll(self._A[: ,col].nonzero()[0], 1)
            down_idx = np.roll(self._A[: ,col].nonzero()[0], -1)
            #print(col, up_idx)
            #print(col, down_idx)

if __name__ == '__main__':
    pass