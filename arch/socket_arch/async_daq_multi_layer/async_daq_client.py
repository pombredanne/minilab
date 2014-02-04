from __future__ import print_function, division
from random import randint

import asyncore
import socket
import sys

sys.path.append('../../../')
from arch.socket_arch.async_analyzer import DaqMultiPlotter
from arch.socket_arch.buffer import DaqDictRingBuffer
from arch.socket_arch.util import extract_channels


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

    def handle_read(self):
        self.cache += self.recv(1024)
        if '\n' in self.cache:
            i = self.cache.index('\n')
            z = len('\n') + i

            data = eval(self.cache[:i])

            self.cache = self.cache[z:]
            print('%s > %s rows received.' % (
                self.internal_id, len(data[data.keys()[0]]) * len(data.keys()))
            )
            self.buffer = self.name

            DaqDictRingBuffer.append(self.name, data)
            DaqDictRingBuffer.status = True

    def readable(self):
        return True

    def writable(self):
        return len(self.buffer) > 0

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


class DaqPlotter(asyncore.dispatcher):
    """

    """
    num_frames = 0

    def __init__(self, num_frames=1000):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.num_frames = num_frames

        DaqMultiPlotter.configure(num_frames)
        DaqMultiPlotter.start()

        DaqDictRingBuffer.status = False

    def handle_close(self):
        DaqMultiPlotter.stop()
        pass

    def readable(self):
        return DaqDictRingBuffer.status

    def handle_read(self):
        data = DaqDictRingBuffer.extract(chunk=self.num_frames)

        DaqMultiPlotter.send_data(data)

        DaqDictRingBuffer.status = False


def start(devices):
    channels = extract_channels(devices)
    samples_per_channel = 100

    DaqDictRingBuffer.configure(samples_per_channel, 0.)
    for name in ['ceramic', 'polymer']:
        DaqDictRingBuffer.bind(name, channels[name])

    ceramic = DaqClient('localhost', 65000, channels['ceramic'], 'ceramic')
    polymer = DaqClient('localhost', 65000, channels['polymer'], 'polymer')
    plotter = DaqPlotter(num_frames=samples_per_channel)

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