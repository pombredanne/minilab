# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function
from collections import defaultdict


class DaqPkgRingBuffer(object):
    """ class that implements a not-yet-full buffer """
    max_limit_package = 5
    data = defaultdict(dict)
    nothing = None
    number_of_lines = 0
    status_buffer = defaultdict(bool)

    @classmethod
    def bind(cls, name, channels):
        """
        @param name: Buffer name
        @type name: str
        @param channels: List of channels of the buffer
        @rtype channels: list
        """
        cls.status_buffer[name] = False
        for channel in channels:
            cls.data[channel][name] = []

    @classmethod
    def configure(cls, max_limit_package, nothing_value):
        """

        """
        cls.max_limit_package = max_limit_package
        cls.nothing = nothing_value

    @classmethod
    def append(cls, new_data):
        """

        """
        for channel in new_data:
            for buffer_name in cls.data[channel]:
                if (
                    len(cls.data[channel][buffer_name]) >=
                        cls.max_limit_package
                ):
                    cls.data[channel][buffer_name].pop(0)
                    print('Data overwritten.')

                cls.data[channel][buffer_name].append(new_data[channel])
                cls.status_buffer[buffer_name] = True

    @classmethod
    def extract_data(cls, buffer_name):
        result = {}

        for channel in cls.data:
            if (
                not buffer_name in cls.data[channel]
                or not cls.data[channel][buffer_name]
            ):
                continue

            result[channel] = cls.data[channel][buffer_name].pop(0)
            cls.status_buffer[buffer_name] = False

        return result if result else None

    @classmethod
    def status(cls, buffer_name):
        return cls.status_buffer[buffer_name]

    @classmethod
    def tolist(cls):
        """ return list of elements in correct order. """
        return cls.data


class DaqDictRingBuffer(object):
    """ class that implements a not-yet-full buffer """
    max_samples_per_channel = 1000
    data = defaultdict(dict)
    nothing = None
    channels = {}
    status_buffer = {}
    overwritten_exception = None

    @classmethod
    def bind(cls, buffer_name, channels):
        """

        """
        cls.channels[buffer_name] = channels
        cls.status_buffer[buffer_name] = False
        for channel in channels:
            cls.data[buffer_name][channel] = (
                [cls.nothing] * cls.max_samples_per_channel
            )

    @classmethod
    def configure(
        cls, max_samples_per_channel,
        nothing_value=0, overwritten_exception=True
    ):
        """ Return a list of elements from the oldest to the newest. """
        cls.max_samples_per_channel = max_samples_per_channel
        cls.nothing = nothing_value
        cls.overwritten_exception = overwritten_exception

    @classmethod
    def append(cls, buffer_name, new_data):
        """ Append an element overwriting the oldest one. """
        for channel in cls.channels[buffer_name]:
            chunk = len(new_data[channel])
            # check if same date will be overwritten
            if cls.overwritten_exception:
                if not all(
                    value == cls.nothing
                    for value in cls.data[buffer_name][channel][:chunk]
                ):
                    raise Exception('Data buffered will be overwritten.')

            del cls.data[buffer_name][channel][:len(new_data[channel])]
            cls.data[buffer_name][channel] += new_data[channel]

    @classmethod
    def extract(cls, buffer_name=None, chunk=1024, start_index=0):
        """ Extract data """
        _data = defaultdict(dict)
        if buffer_name:
            for channel in cls.data[buffer_name]:
                _data[channel] = (
                    cls.data[buffer_name][channel][start_index:chunk]
                )

                cls.data[buffer_name][channel][:chunk+start_index] = (
                    [cls.nothing] * (chunk + start_index)
                )
        else:
            for buffer_name in cls.data:
                _data[buffer_name] = {}
                for channel in cls.data[buffer_name]:
                    _data[buffer_name][channel] = (
                        cls.data[buffer_name][channel][start_index:chunk]
                    )

                    cls.data[buffer_name][channel][:chunk+start_index] = (
                        [cls.nothing] * (chunk + start_index)
                    )

        return _data

    @classmethod
    def status(cls, buffer_name=None, status=None):
        """

        """
        if not buffer_name and status is None:
            return cls.status_buffer.values()

        if not buffer_name:
            for n in cls.status_buffer:
                cls.status_buffer[n] = status
            return

        cls.status_buffer[buffer_name] = status

    @classmethod
    def tolist(cls):
        """ return list of elements in correct order. """
        return cls.data

if __name__ == '__main__':
    def test1():
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

        MAX_LINES_BUFFER = 10
        MAX_LINES = 5

        x = DaqDictRingBuffer
        x.configure(10, 0.0)
        x.bind('ceramic', ['Dev1/ai0', 'Dev1/ai1', 'Dev1/ai2', 'Dev1/di0'])

        devices = {
            'Dev1/di0': [0]*MAX_LINES,
            'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
        }

        x.append('ceramic', devices)
        print(x.__class__, x.tolist())

        devices = {
            'Dev1/di0': [0]*MAX_LINES,
            'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
        }

        x.append('ceramic', devices)
        print(x.__class__, x.tolist())

        print(x.extract('ceramic', 5))

    def test2():
        # internal
        import sys
        import platform

        if platform.system() == 'Linux':
            sys.path.append('/var/www/mswim/')
        else:
            sys.path.append('c:/mswim/')

        from mswim.settings import DEVICES as SENSORS_GROUP
        from util import extract_devices, extract_channels

        devices = extract_devices(SENSORS_GROUP)
        channels = extract_channels(SENSORS_GROUP)

        x = DaqPkgRingBuffer
        x.configure(7, 0.0)

        for name in channels:
            x.bind(name, channels[name])

        x.append({'Dev4/ai30': [1, 2, 3, 4, 5], 'Dev4/ai31': [6, 7, 8, 9, 0]})
        print(x.tolist())

        data = x.extract_data('ceramic')
        print('extracted data:')
        print(data)

        data = x.extract_data('ceramic')
        print('extracted data:')
        print(data)

        x.append({'Dev5/ai1': [1, 2, 3, 4, 5], 'Dev5/ai2': [6, 7, 8, 9, 0]})
        data = x.extract_data('ceramic')
        print('extracted data:')
        print(data)

    test1()