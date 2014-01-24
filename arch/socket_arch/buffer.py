# -*- coding: utf-8 -*-
"""

"""


class DaqRingBuffer(object):
    """ class that implements a not-yet-full buffer """
    max = 5
    data = []
    nothing = None

    @classmethod
    def limit_max(cls, cols, max_rows):
        """ Return a list of elements from the oldest to the newest. """
        cls.max = max
        cls.data = [[cls.nothing] * max_rows] * cols

    @classmethod
    def nothing_value(cls, nothing):
        """ Return a list of elements from the oldest to the newest. """
        cls.nothing = nothing

    @classmethod
    def append(cls, new_data):
        """ Append an element overwriting the oldest one. """

        for key, col_data in enumerate(cls.data):
            cls.data[key] = cls.data[key][len(new_data[key]):] + new_data[key]

    @classmethod
    def tolist(cls):
        """ return list of elements in correct order. """
        return cls.data

# sample usage
if __name__ == '__main__':
    x = DaqRingBuffer

    x.limit_max(2, 4)
    print x.__class__, x.tolist()

    x.append([[1, 2], [3, 4]])
    print x.__class__, x.tolist()

    x.append([[2, 3], [4, 5]])
    print x.__class__, x.tolist()

    x.append([[3, 4], [5, 6]])
    print x.__class__, x.tolist()

    x.append([[4, 5], [6, 7]])
    print x.__class__, x.tolist()
