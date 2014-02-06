from __future__ import print_function, division
from random import randint

import sys
import asyncore
import socket
import platform
from time import sleep

# internal
sys.path.append('../../../')
from arch.socket_arch.async_plotter import plt_start, plt_stop, plt_plotter
from arch.socket_arch.buffer import DaqDictRingBuffer
from arch.socket_arch.util import extract_channels


class DaqClient(asyncore.dispatcher):

    def __init__(self, host, port, device, daq_name):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = str(device)
        self.cache = ''
        self.name = daq_name
        self.internal_id = randint(0, 1000000)

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        self.cache += self.recv(1024)

        if '\n' in self.cache:
            i = self.cache.index('\n')
            z = len('\n') + i

            print('Received %s bytes.' % len(self.cache[:i]))

            data = eval(self.cache[:i])
            self.cache = self.cache[z:]
            #print('%s > %s rows received.' % (self.internal_id, len(data[0])))

            DaqDictRingBuffer.append(self.name, data)
            DaqDictRingBuffer.status = True

            self.buffer += '.'

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
        self.plotter = plt_start(DaqDictRingBuffer.number_of_lines)
        DaqDictRingBuffer.status = False

    def handle_close(self):
        plt_stop()
        pass

    def readable(self):
        return DaqDictRingBuffer.status

    def handle_read(self):
        plt_plotter(DaqDictRingBuffer.data, self.plotter)
        DaqDictRingBuffer.status = False


def start(sensors_groups):
    channels = extract_channels(sensors_groups)
    DaqDictRingBuffer.configure(100000, 0.)

    for name in ['ceramic']:
        DaqDictRingBuffer.bind(name, channels[name])

    ceramic = DaqClient('localhost', 65000, channels['ceramic'], 'ceramic')
    #polymer = DaqClient('localhost', 65000, devices['polymer'])
    #plotter = DaqPlotter()

    asyncore.loop()

if __name__ == '__main__':
    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim import settings
    start(settings.DEVICES)