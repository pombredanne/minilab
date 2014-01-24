from random import randint

import sys
import asyncore
import socket
import platform
from time import sleep

# internal
if platform.system() == 'Linux':
    sys.path.append('/var/www/mswim/')
else:
    sys.path.append('c:/mswim/')

from mswim import settings
from async_analyzer import plt_start, plt_stop, plt_plotter
from buffer import DaqRingBuffer


class DaqClient(asyncore.dispatcher):

    def __init__(self, host, port, device):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((host, port))
        self.buffer = str(device)
        self.cache = ''
        self.internal_id = randint(0, 1000000)
        self.plotter = plt_start()

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
            print('%s > %s rows received.' % (self.internal_id, len(data[0])))
            self.buffer += '.'

            DaqRingBuffer.append(data)
            print(
                '%s > Buffer %s data registered.' %
                (self.internal_id, len(DaqRingBuffer.data))
            )

            #plt_plotter(data, self.plotter)
            #print('%s > plotted.' % (self.internal_id))

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
        self.plotter = plt_start()

    def handle_close(self):
        plt_stop()

    def handle_read(self):
        plt_plotter(DaqRingBuffer.data, self.plotter)
        sleep(0.02)
        pass


def start(devices):
    ceramic = DaqClient('localhost', 65000, devices['ceramic'])
    polymer = DaqClient('localhost', 65000, devices['polymer'])
    plotter = DaqPlotter()

    DaqRingBuffer.nothing_value(0)
    DaqRingBuffer.limit_max(16, 1000)

    asyncore.loop()

if __name__ == '__main__':
    start(settings.DEVICES)