from __future__ import print_function, division
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
from async_plotter import plt_start, plt_stop, plt_plotter


class ClientSimple(asyncore.dispatcher):
    """

    """
    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = True
        print('Started.')

    def handle_close(self):
        print('Closed.')
        pass

    def readable(self):
        print('doing something')
        sleep(2)
        return self.status

    def writable(self):
        return False

    def handle_read(self):
        data = self.recv(1024)
        print('read handled.')
        self.status = False

    def handle_write(self):
        print('write handled.')

    def handle_error(self):
        print('Error handled.')

    def handle_expt(self):
        print('expt handled.')


def start(devices):
    client = ClientSimple()

    asyncore.loop(timeout=0.0)

if __name__ == '__main__':
    start(settings.DEVICES)