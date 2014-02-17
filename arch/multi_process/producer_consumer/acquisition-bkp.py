# -*- coding: utf-8 -*-
from __future__ import print_function
from multiprocessing import Pool
from time import sleep
from collections import defaultdict

import sys
import time
import os

sys.path.append('../../../')
from arch.socket_arch.buffer import DaqDictRingBuffer, DaqPkgRingBuffer
from arch.socket_arch.util import extract_channels, extract_devices
from arch.socket_arch.segmentation import SegmentedByTrigger
from arch.socket_arch.weigh import Weigh

from daq_server import DaqRegister, DaqServer
from daq_analyzer import DaqAnalyzer, DaqAsyncPlotter, DaqPlotter

import psutil


def memory_usage():
    """
    Return memory usage in MB unity.
    """
    process = psutil.Process(os.getpid())
    return process.get_memory_info()[0]/float(2**20)


def process_next(routine):
    print('...')
    return routine.read()


def loop(routines=[], wait=0.):
    """
    Loop of routines using coroutines structure

    @param routines: List of functions
    @type routines: object
    @param wait: Seconds to wait after each function called
    @type wait: float

    """
    print('Starting acquisition.')

    pool = Pool(processes=10)  # start 4 worker processes

    while True:
        if memory_usage() >= 1280:
            raise Exception('Memory usage exceed.')

        time_0 = time.time()

        data = pool.map(process_next, routines)

        print('%f' % (time.time() - time_0))
        exit()


def startup(sensors_groups):
    """

    """
    server = []
    client = []

    # total samples per channel
    samples_per_channel = 15000
    # samples per channel per each read access
    samples_per_channel_read = 1000
    # quantity of package of data to be buffered
    packages_per_channel = 1

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)
    tree_channels = defaultdict(dict)

    DaqPkgRingBuffer.configure(packages_per_channel, 0.0)
    DaqDictRingBuffer.configure(
        max_samples_per_channel=samples_per_channel*2,
        nothing_value=0,
        overwritten_exception=False
    )

    # server daq configurations
    for name in channels:
        DaqPkgRingBuffer.bind(name, channels[name])

    for name in devices:
        # Server routines
        server.append(
            DaqRegister(devices[name], samples_per_channel_read)
        )

    # client analyzer configurations
    for name in channels:
        tree_channels[name] = dict([(ch, None) for ch in channels[name]])
        DaqDictRingBuffer.bind(name, channels[name])

        # Client routines
        client.append(
            DaqAnalyzer(
                channels=channels[name],
                daq_name=name,
                server=DaqServer.listening(channels[name], name)
            )
        )

    """
    # View all signals ring buffer
    chart = DaqPlotter(samples_per_channel=samples_per_channel*2)
    client.append(chart)
    """

    # View only segmented signals
    chart = DaqAsyncPlotter(
        samples_per_channel=samples_per_channel, tree_channels=tree_channels
    )
    #client.append(chart)

    def callback_process(data):
        # call the weigh method
        weight = Weigh.calculate(data)

        # call the save method
        #
        # call chart method
        chart.send(data)

    # Segmentation Module
    for name in channels:
        client.append(
            SegmentedByTrigger(
                buffer_name=name,
                channels=channels[name],
                trigger=sensors_groups[name]['trigger'],
                chunk=samples_per_channel,
                ring_buffer=DaqDictRingBuffer,
                callback=callback_process
            )
        )
    loop(routines=server+client, wait=0.00000001)

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