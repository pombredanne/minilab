# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function
from collections import defaultdict


class DaqRingBuffer(object):
    """ class that implements a not-yet-full buffer """
    max = 5
    data = []
    nothing = None
    number_of_lines = 0

    @classmethod
    def limit_max(cls, number_of_lines, max_rows):
        cls.max = max
        cls.number_of_lines = number_of_lines
        cls.data = [[cls.nothing] * max_rows] * number_of_lines

    @classmethod
    def nothing_value(cls, nothing):
        cls.nothing = nothing

    @classmethod
    def append(cls, new_data):
        for key, col_data in enumerate(cls.data):
            cls.data[key] = cls.data[key][len(new_data[key]):] + new_data[key]

    @classmethod
    def tolist(cls):
        """ return list of elements in correct order. """
        return cls.data


class DaqDictRingBuffer(object):
    """ class that implements a not-yet-full buffer """
    max_lines = 1000
    data = defaultdict(list)
    nothing = None
    number_of_cols = 0

    @classmethod
    def configure(cls, ordered_keys, max_lines):
        """ Return a list of elements from the oldest to the newest. """
        cls.max_lines = max_lines
        cls.number_of_cols = len(ordered_keys)

        for device in ordered_keys:
            for key in ordered_keys[device]:
                cls.data[key] = [cls.nothing] * max_lines

    @classmethod
    def nothing_value(cls, nothing):
        """ Return a list of elements from the oldest to the newest. """
        cls.nothing = nothing

    @classmethod
    def append(cls, new_data):
        """ Append an element overwriting the oldest one. """
        for position, key in enumerate(cls.data):
            cls.data[key] = (
                cls.data[key][len(new_data[key]):] + new_data[key]
            )

    @classmethod
    def extract(cls, start_position, end_position):
        """ Extract data """
        _data = defaultdict(list)
        for position, key in enumerate(cls.data):

            _data[key] = (
                cls.data[key][start_position:end_position]
            )

            cls.data[key][:end_position] = (
                [cls.nothing] * len(cls.data[key][:end_position])
            )

        return _data

    @classmethod
    def tolist(cls):
        """ return list of elements in correct order. """
        return cls.data

# sample usage
if __name__ == '__main__':
    from random import random

    channels = [
        dict(
            [('Dev1/ai%s' % sen, sen) for sen in range(3)] +
            [('Dev1/di0', 3)]
        )
    ]

    sorted_channels = {}

    for _id, chans in enumerate(channels):
        sorted_channels[_id] = [
            c for c in sorted(
                chans, key=lambda x: chans[x]
            )
        ]

    MAX_LINES_BUFFER = 2
    MAX_LINES = 1

    x = DaqDictRingBuffer
    x.configure(sorted_channels, MAX_LINES_BUFFER)

    devices = {
        'Dev1/di0': [0]*MAX_LINES,
        'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
    }

    x.append(devices)
    print(x.__class__, x.tolist())

    devices = {
        'Dev1/di0': [0]*MAX_LINES,
        'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
    }

    x.append(devices)
    print(x.__class__, x.tolist())
