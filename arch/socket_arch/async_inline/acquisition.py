# -*- coding: utf-8 -*-
from __future__ import print_function
import asyncore
import socket

import sys

sys.path.append('../../../')
from arch.socket_arch.buffer import DaqDictRingBuffer, DaqPkgRingBuffer
from arch.socket_arch.util import extract_channels, extract_devices

from daq_server import DaqRegister, DaqServer
from daq_analyzer import DaqAnalyzer, DaqPlotter


def startup(sensors_groups, host='localhost', port=65000):
    """

    """
    server = []
    client = []

    samples_per_channel = 100

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)

    DaqPkgRingBuffer.configure(samples_per_channel, 0.0)
    DaqDictRingBuffer.configure(samples_per_channel*10, 0)

    # server daq configurations
    for name in channels:
        DaqPkgRingBuffer.bind(name, channels[name])

    for name in devices:
        server.append(DaqRegister(devices[name]))

    server.append(DaqServer(host, port))

    # client analyzer configurations
    for name in channels:
        DaqDictRingBuffer.bind(name, channels[name])
        client.append(
            DaqAnalyzer('localhost', 65000, channels['ceramic'], name)
        )

    client.append(DaqPlotter(samples_per_channel=samples_per_channel*10))

    asyncore.loop()

if __name__ == '__main__':
    def test():
        """

        """
        import sys
        import platform

        # internal
        if platform.system() == 'Linux':
            sys.path.append('/var/www/mswim/')
        else:
            sys.path.append('c:/mswim/')

        from mswim.settings import DEVICES as SENSORS_GROUP

        startup(SENSORS_GROUP)

    test()