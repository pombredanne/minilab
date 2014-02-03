from __future__ import print_function, division
from random import randint

import asyncore
import socket

from ..async_analyzer import plt_start, plt_stop, plt_plotter
from ..buffer import DaqDictRingBuffer
from ..util import extract_channels


class DaqAnalyze(asyncore.dispatcher):

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
        #self.close()
        pass

    def handle_read(self):
        self.cache += self.recv(1024)
        print(len(self.cache))
        if '\n' in self.cache:
            i = self.cache.index('\n')
            z = len('\n') + i

            self.cache[:i]

            data = eval(self.cache[:i])

            print(data)

            self.cache = self.cache[z:]
            print('%s > %s rows received.' % (self.internal_id, len(data[0])))
            self.buffer = str(self.channels)

            DaqDictRingBuffer.append(self.name, data)
            DaqDictRingBuffer.status = True

            print(
                '%s > Buffer %s data registered.' %
                (self.internal_id, len(DaqDictRingBuffer.data))
            )

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
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.plotter = plt_start(DaqDictRingBuffer.max_samples_per_channel)
        DaqDictRingBuffer.status = False

    def handle_close(self):
        plt_stop()
        pass

    def readable(self):
        return DaqDictRingBuffer.status

    def handle_read(self):
        plt_plotter(DaqDictRingBuffer.data, self.plotter)
        DaqDictRingBuffer.status = False


def start(devices):
    DaqDictRingBuffer.configure(1000, 0)
    channels = extract_channels(devices)

    ceramic = DaqAnalyze('localhost', 65000, channels['ceramic'], 'ceramic')
    #polymer = DaqClient('localhost', 65000, channels['polymer'], 'polymer')
    #plotter = DaqPlotter()

    asyncore.loop(0.1)

if __name__ == '__main__':
    # internal
    import sys
    import platform

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim import settings
    start(settings.DEVICES)