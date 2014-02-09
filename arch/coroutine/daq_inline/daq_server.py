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


class DaqRegister(object):
    """
    Socket class to register, process and return data from Acquisition Tasks

    """
    device = ''

    def __init__(self, device):
        """

        """
        self.device = device

        self.daq = AcquisitionTask(device, 'continuous', 15000)
        print('Device %s is initialized' % device['name'])

    def read(self):
        DaqPkgRingBuffer.append(self.daq.read())
        return True


class DaqServer(object):
    """
    Connect client with server using coroutine method listening

    """
    @classmethod
    def listening(cls, channels, daq_id):
        while True:
            yield DaqPkgRingBuffer.extract_data(daq_id)

if __name__ == '__main__':
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

    # internal
    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim.settings import DEVICES as SENSORS_GROUP

    startup(SENSORS_GROUP)