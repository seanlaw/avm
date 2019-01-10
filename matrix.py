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
        self._generalize()

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

    def _generalize(self):
        if self.secondary_idx is not None:
            for col in self.secondary_idx:
                col_header = self.column_headers[col]
                col_header.L = col_header
                col_header.R = col_header

if __name__ == '__main__':
    pass