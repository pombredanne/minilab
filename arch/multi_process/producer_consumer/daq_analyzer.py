from __future__ import print_function, division
from random import randint
from collections import defaultdict

import asyncore
import socket
import sys

sys.path.append('../../../')
from arch.socket_arch.async_plotter import DaqMultiPlotter
from arch.socket_arch.buffer import DaqDictRingBuffer
from arch.socket_arch.util import extract_channels


class DaqAsyncTurn(object):
    """
    Controls the async process ordered.

    """
    daq_list = []
    position = 0

    @classmethod
    def bind(cls, daq_name):
        """
        Sets a DAQ list processes.

        """
        cls.daq_list += [daq_name]

    @classmethod
    def is_my_turn(cls, daq_name):
        """
        Checks if now is the turn of DAQ informed.

        """
        return cls.daq_list.index(daq_name) == cls.position

    @classmethod
    def next_turn(cls):
        """
        Go to the next turn of the DAQ list.

        """
        cls.position = (
            cls.position + 1 if cls.position + 1 < len(cls.daq_list) else 0
        )


class DaqPlotter():
    """

    """
    num_frames = 0

    def __init__(self, samples_per_channel=1000):
        self.samples_per_channel = samples_per_channel
        self.name = 'plotter'

        DaqAsyncTurn.bind(self.name)

        DaqMultiPlotter.configure(samples_per_channel)
        DaqMultiPlotter.start()

    def read(self):
        if DaqAsyncTurn.is_my_turn(self.name):
            data = DaqDictRingBuffer.tolist()

            DaqMultiPlotter.send_data(data)

            # Wait for new data on Ring Buffer
            DaqDictRingBuffer.status(status=False)
            DaqAsyncTurn.next_turn()


class DaqAsyncPlotter():
    """

    """
    num_frames = 0
    data = {}

    def __init__(self, samples_per_channel=15000, tree_channels={}):
        self.samples_per_channel = samples_per_channel
        self.name = 'async-plotter'
        self.data = defaultdict(dict)

        for group_name in tree_channels:
            for channel_name in tree_channels[group_name]:
                self.data[group_name][channel_name] = [0] * samples_per_channel

        DaqAsyncTurn.bind(self.name)

        DaqMultiPlotter.configure(samples_per_channel)
        DaqMultiPlotter.start()

    def send(self, data):
        """

        """
        for name in data:
            self.data[name] = data[name]

    def read(self):
        if DaqAsyncTurn.is_my_turn(self.name):
            DaqMultiPlotter.send_data(self.data)

            # Wait for new data on Ring Buffer
            DaqDictRingBuffer.status(status=False)
            DaqAsyncTurn.next_turn()

if __name__ == '__main__':
    def start(devices):
        channels = extract_channels(devices)
        samples_per_channel = 100

        DaqDictRingBuffer.configure(samples_per_channel, 0.)
        groups = ['ceramic', 'polymer']
        for name in groups:
            DaqDictRingBuffer.bind(name, channels[name])

        plotter = DaqPlotter(samples_per_channel=samples_per_channel)

        asyncore.loop()

    # internal
    import sys
    import platform
    import pickle

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim import settings
    start(settings.DEVICES)