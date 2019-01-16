#!/usr/bin/env python

class ROOT(object):
    """
    Base class
    """

    def __init__(self):
        self._left = self
        self._right = self
 
    @property
    def L(self):
        return self._left

    @L.setter
    def L(self, value):
        self._left = value

    @property
    def R(self):
        return self._right

    @R.setter
    def R(self, value):
        self._right = value

    def sweep(self, direction_attr):
        x = getattr(self, direction_attr)
        while x != self:
            yield x
            x = getattr(x, direction_attr)
        else:
            return

class DATA(ROOT):
    """
    Data Object that inherits from ROOT base class
    """

    def __init__(self):
        super().__init__()
        self._up = self
        self._down = self
        self._column = self
        self._row = self

    @property
    def U(self):
        return self._up

    @U.setter
    def U(self, value):
        self._up = value

    @property
    def D(self):
        return self._down

    @D.setter
    def D(self, value):
        self._down = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, value):
        self._row = value

class COLUMN(ROOT):
    """
    Column Object that inherits from LINKED_LIST base class
    """

    def __init__(self):
        super().__init__()
        self._up = self
        self._column = self
        self._size = None
        self._name = None

    @property
    def U(self):
        return self._up

    @U.setter
    def U(self, value):
        self._up = value

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, value):
        self._column = value

    @property
    def S(self):
        return self._size

    @S.setter
    def S(self, value):
        self._size = value

    @property
    def N(self):
        return self._name

    @N.setter
    def N(self, value):
        self._name = value

if __name__ == '__main__':
    root = ROOT()
    data = DATA()
    column = COLUMN()