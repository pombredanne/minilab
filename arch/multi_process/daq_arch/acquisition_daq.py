# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep
from datetime import timedelta
from collections import defaultdict
from multiprocessing import Pool
import time

import psutil
import os
import sys

sys.path.insert(0, '/var/www/mswim/')

from acquisition.util.buffer import DaqDictRingBuffer, DaqPkgRingBuffer
from acquisition.util.daq_util import extract_channels, extract_devices

from acquisition.segmentation import SegmentedByTrigger
from acquisition.weigh import Weigh

from arch.multi_process.daq_arch.daq_server import DaqRegister, DaqServer
from arch.multi_process.daq_arch.daq_analyzer import DaqAnalyzer, DaqAsyncPlotter, DaqPlotter

from mswim.apps.acquisition.models import save_acquisition_data

SERVER = []
CLIENT = []
PROCESS = []


def memory_usage():
    """
    Return memory usage in MB unity.
    """
    process = psutil.Process(os.getpid())
    return process.get_memory_info()[0] / float(2 ** 20)


def run_server(pid):
    return SERVER[pid].read()


def run_client(pid):
    return CLIENT[pid].read()


def run_process(pid):
    return PROCESS[pid].read()


def loop(servers=[], clients=[], processes=[], wait=0.):
    """
    Loop of routines using coroutines structure

    @param routines: List of functions
    @type routines: object
    @param wait: Seconds to wait after each function called
    @type wait: float

    """
    print('Starting acquisition.')
    SERVER[:] = servers
    CLIENT[:] = clients
    PROCESS[:] = processes

    servers_range = range(len(servers))
    clients_range = range(len(clients))
    processes_range = range(len(processes))

    pool = Pool(processes=10)  # start 4 worker processes

    while True:
        if memory_usage() >= 1280:
            raise Exception('Memory usage exceed.')

        time_0 = time.time()

        pool.map(run_server, servers_range)
        pool.map(run_client, clients_range)
        pool.map(run_process, processes_range)

        print('%f' % (time.time() - time_0))
        time.sleep(wait)


def startup(sensors_groups):
    """

    """
    server = []
    client = []
    process = []

    # total samples per channel
    samples_per_channel = 15000
    # samples per channel per each read access
    samples_per_channel_read = 1000
    # quantity of package of data to be buffered
    packages_per_channel = 100

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)
    tree_channels = defaultdict(dict)

    DaqPkgRingBuffer.configure(packages_per_channel, 0.0)
    DaqDictRingBuffer.configure(
        max_samples_per_channel=samples_per_channel * 2,
        nothing_value=0,
        overwritten_exception=False
    )

    # Server DAQ configurations
    for name in channels:
        DaqPkgRingBuffer.bind(name, channels[name])

    for name in devices:
        server.append(DaqRegister(devices[name], samples_per_channel_read))

    # Client analyzer configurations
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


    # View all signals ring buffer
    chart = DaqPlotter(samples_per_channel=samples_per_channel*2)
    process.append(chart)


    # View only segmented signals
    """
    chart = DaqAsyncPlotter(
        samples_per_channel=samples_per_channel, tree_channels=tree_channels
    )
    client.append(chart)
    """

    def callback_process(data):
        # TODO: Re-factor it
        group_name = data.keys()[0]
        group_channels = sensors_groups[group_name]['channels']

        temperature_channels = dict(
            [(str(v), i) for i, v in
             sensors_groups[group_name]['temperature_channels'][0].items()
            ]
        )

        # call the weigh method
        weight = Weigh.calculate(data)
        # call the save method
        save_acquisition_data(data, group_channels, temperature_channels)
        # call chart method
        # chart.send(data)

    """
    # Segmentation Module
    for name in channels:
        if not sensors_groups[name]['trigger']:
            continue

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
    """
    try:
        loop(servers=server, clients=client, processes=process, wait=0.0001)
    except KeyboardInterrupt:
        print('\nAcquisition was closed.')
        exit()


def main():
    """

    """
    import sys

    # internal
    sys.path.append('/var/www/mswim/')

    from mswim.settings import DEVICES as SENSORS_GROUP
    from mswim.libs.db import conn

    # active the database connection
    conn.Pool.connect()

    startup(SENSORS_GROUP)


if __name__ == '__main__':
    main()
