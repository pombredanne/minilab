# -*- coding: utf-8 -*-
from __future__ import print_function
import asyncore
import socket

from ..async_analyzer import plt_start, plt_stop, plt_plotter
from ..buffer import DaqDictRingBuffer, DaqPkgRingBuffer
from ..util import extract_devices, extract_channels

from daq_server import DaqRegister, DaqServer
from daq_analyze import DaqAnalyze


def startup(sensors_groups, host='localhost', port=65000):
    """

    """
    server = []

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)
    DaqPkgRingBuffer.configure(10, 0.0)

    for name in channels:
        DaqPkgRingBuffer.bind(name, channels[name])

    for name in devices:
        server.append(DaqRegister(devices[name]))

    server.append(DaqServer(host, port))
    DaqDictRingBuffer.configure(1000, 0)
    channels = extract_channels(devices)

    ceramic = DaqAnalyze('localhost', 65000, channels['ceramic'], 'ceramic')
    #polymer = DaqClient('localhost', 65000, channels['polymer'], 'polymer')
    #plotter = DaqPlotter()

if __name__ == '__main__':
    import sys
    import platform

    # internal
    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim.settings import DEVICES as SENSORS_GROUP

    startup(SENSORS_GROUP)