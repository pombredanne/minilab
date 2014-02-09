# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep
from collections import defaultdict

import asyncore
import socket
import sys
import resource

sys.path.append('../../../')
from arch.socket_arch.buffer import DaqDictRingBuffer, DaqPkgRingBuffer
from arch.socket_arch.util import extract_channels, extract_devices
from arch.socket_arch.segmentation import SegmentedByTrigger

from daq_server import DaqRegister, DaqServer
from daq_analyzer import DaqAnalyzer, DaqAsyncPlotter


def memory_usage():
    """
    Return memory usage in MB unity.
    """
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024


def loop(routines=[], wait=0.):
    """
    Loop of routines using coroutines structure

    @param routines: List of functions
    @type routines: object
    @param wait: Seconds to wait after each function called
    @type wait: float

    """
    while True:
        for routine in routines:
            if memory_usage() >= 1024:
                raise Exception('Memory usage exceed.')
            routine.read()
            sleep(wait)


def startup(sensors_groups):
    """

    """
    server = []
    client = []

    samples_per_channel = 15000
    packages_per_channel = 100

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)
    tree_channels = defaultdict(dict)

    DaqPkgRingBuffer.configure(packages_per_channel, 0.0)
    DaqDictRingBuffer.configure(
        max_samples_per_channel=samples_per_channel*3,
        nothing_value=0,
        overwritten_exception=False
    )

    # server daq configurations
    for name in channels:
        DaqPkgRingBuffer.bind(name, channels[name])

    for name in devices:
        server.append(DaqRegister(devices[name]))

    # client analyzer configurations
    for name in channels:
        tree_channels[name] = dict([(ch, None) for ch in channels[name]])
        DaqDictRingBuffer.bind(name, channels[name])

        client.append(
            DaqAnalyzer(
                channels=channels[name],
                daq_name=name,
                server=DaqServer.listening(channels[name], name)
            )
        )

    chart = DaqAsyncPlotter(
        samples_per_channel=samples_per_channel, tree_channels=tree_channels
    )
    client.append(chart)

    # Segmentation Module
    for name in channels:
        #print(channels[name])
        #print(sensors_groups[name]['trigger'])
        client.append(
            SegmentedByTrigger(
                buffer_name=name,
                channels=channels[name],
                trigger=sensors_groups[name]['trigger'],
                chunk=15000,
                ring_buffer=DaqDictRingBuffer,
                callback=chart.send
            )
        )
    loop(server+client)

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