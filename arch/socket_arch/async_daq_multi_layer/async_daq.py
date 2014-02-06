# -*- coding: utf-8 -*-
"""
Async module to server data from Acquisition Tasks through Ring Buffers

"""
from __future__ import print_function, division
from random import randint
from time import sleep

import asyncore
import socket
import sys
import platform

# internal
sys.path.append('../../../')
from daq.ni.acquisition import AcquisitionTask
from arch.socket_arch.util import extract_devices, extract_channels
from arch.socket_arch.buffer import DaqPkgRingBuffer


class DaqRegister(asyncore.dispatcher):
    """
    Socket class to register, process and return data from Acquisition Tasks

    """
    device = ''

    def __init__(self, device):
        """

        """
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device = device

        self.daq = AcquisitionTask(device, 'continuous', 100)
        print('Device %s is initialized' % device['name'])

    def readable(self):
        DaqPkgRingBuffer.append(self.daq.read())
        return True


class DaqServerHandler(asyncore.dispatcher_with_send):
    """
    Handler used to sends data to DAQ Clients

    """
    def __init__(self, conn_sock, client_address):
        self.client_address = client_address
        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        self.channels = []
        self.out_buffer = ''
        self.daq_id = ''
        print('DAQ Server initialized')

    def handle_connect(self):
        print('Connection established.')

    def writable(self):
        return True

    def readable(self):
        return True

    def handle_read(self):
        data = self.recv(8192)

        if data:
            if not self.channels:
                self.daq_id, self.channels = eval(data)

            _buffer = str(DaqPkgRingBuffer.extract_data(self.daq_id)) + '\n'
            print('sending %s bytes' % len(_buffer))
            self.send(_buffer)


class DaqServer(asyncore.dispatcher):
    """
    Daq Server provides data to DAQ Client from Ring Buffer

    """
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print('DAQ Server initialized')

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            print('Incoming connection from %s' % repr(address))
            handler = DaqServerHandler(sock, address)


def startup(sensors_groups, host='localhost', port=65000):
    """

    """
    server = []

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)
    DaqPkgRingBuffer.configure(100, 0.0)

    for name in channels:
        DaqPkgRingBuffer.bind(name, channels[name])

    for name in devices:
        server.append(DaqRegister(devices[name]))

    server.append(DaqServer(host, port))

    asyncore.loop(0.5)

if __name__ == '__main__':
    # internal
    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim.settings import DEVICES as SENSORS_GROUP

    startup(SENSORS_GROUP)