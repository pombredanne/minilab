# -*- coding: utf-8 -*-
"""
Receive from client socket a list of channels and sends saved signals,
from older acquisitions, and assigned to each channel from the list

"""
from random import random
from collections import defaultdict

import asyncore
import socket
import sys

# internal
sys.path.append('../../../')
from arch.socket_arch.db import simulate_daq


class DAQ():
    """

    """
    def __init__(self, samples_per_channel=1000):
        self.devices = None
        self.sensors = None
        self.channels = None
        self.number_of_channels = 0
        self.samples_per_channel = samples_per_channel
        self.daq = None

    def register_devices(self, channels, settings):
        """

        """
        self.number_of_channels += len(channels)
        self.channels = channels
        self.daq = simulate_daq(settings, self.samples_per_channel)
        self.daq.next()
        self.daq.send((channels, self.samples_per_channel))

    def read(self):
        data = self.read_db()

        return dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.channels)
        ])

    def read_db(self):
        return self.daq.next()

    def read_random(self):
        """

        """
        data = []
        for _ in xrange(self.number_of_channels):
            data.append([random() for _ in xrange(self.samples_per_channel)])
        return data


class DaqHandler(asyncore.dispatcher_with_send):
    """

    """
    def __init__(self, conn_sock, client_address, settings):
        self.client_address = client_address
        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        self.out_buffer = ''
        self.daq = DAQ(5000)
        self.settings = settings

    def handle_read(self):
        data = self.recv(8192)

        if data:
            if not self.daq.channels:
                channels = eval(data)
                self.daq.register_devices(channels, self.settings)
            self.send(str(self.daq.read()) + '\n')


class DaqServer(asyncore.dispatcher):
    """

    """
    def __init__(self, host, port, settings):
        """

        """
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        self.settings = settings

    def handle_accept(self):
        """

        """
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            print 'Incoming connection from %s' % repr(address)
            handler = DaqHandler(sock, address, self.settings)


if __name__ == '__main__':
    # internal
    import sys
    import platform

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim import settings as _settings

    server = DaqServer('localhost', 65000, _settings)
    asyncore.loop()