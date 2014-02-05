from __future__ import print_function, division
from random import randint

import asyncore
import socket
import sys

sys.path.append('../../../')
from arch.socket_arch.async_analyzer import DaqMultiPlotter
from arch.socket_arch.buffer import DaqDictRingBuffer
from arch.socket_arch.util import extract_channels


class DaqAsyncTurn(object):
    """
    Controls the async process ordered.

    """
    daq_list = None
    position = 0

    @classmethod
    def configure(cls, daq_list):
        """
        Sets a DAQ list processes.

        """
        cls.daq_list = daq_list

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


class DaqClient(asyncore.dispatcher):

    def __init__(self, host, port, channels, daq_name):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.channels = channels
        self.buffer = str((daq_name, channels))
        self.cache = ''
        self.internal_id = randint(0, 1000000)
        self.name = daq_name

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def readable(self):
        return DaqAsyncTurn.is_my_turn(self.name)

    def handle_read(self):
        if DaqAsyncTurn.is_my_turn(self.name):
            self.cache += self.recv(1024)
            if '\n' in self.cache:
                i = self.cache.index('\n')
                z = len('\n') + i

                data = eval(self.cache[:i])

                self.cache = self.cache[z:]
                print('%s > %s samples per channel received.' % (
                    self.name, len(data[data.keys()[0]]))
                )
                self.buffer = self.name

                DaqDictRingBuffer.append(self.name, data)
                DaqAsyncTurn.next_turn()

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


class DaqPlotter(asyncore.dispatcher):
    """

    """
    num_frames = 0

    def __init__(self, samples_per_channel=1000):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.samples_per_channel = samples_per_channel
        self.name = 'plotter'

        DaqMultiPlotter.configure(samples_per_channel)
        DaqMultiPlotter.start()

    def handle_expt(self):
        DaqMultiPlotter.stop()

    def handle_close(self):
        DaqMultiPlotter.stop()

    def readable(self):
        return DaqAsyncTurn.is_my_turn(self.name)

    def handle_read(self):
        if DaqAsyncTurn.is_my_turn(self.name):
            data = DaqDictRingBuffer.extract(chunk=self.samples_per_channel)

            DaqMultiPlotter.send_data(data)

            # Wait for new data on Ring Buffer
            DaqDictRingBuffer.status(status=False)
            DaqAsyncTurn.next_turn()


def start(devices):
    channels = extract_channels(devices)
    samples_per_channel = 100

    DaqDictRingBuffer.configure(samples_per_channel*20, 0.)
    groups = ['ceramic', 'polymer']
    for name in groups:
        DaqDictRingBuffer.bind(name, channels[name])

    DaqAsyncTurn.configure(groups + ['plotter'])

    ceramic = DaqClient('localhost', 65000, channels['ceramic'], 'ceramic')
    polymer = DaqClient('localhost', 65000, channels['polymer'], 'polymer')
    plotter = DaqPlotter(samples_per_channel=samples_per_channel)

    asyncore.loop()

if __name__ == '__main__':
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