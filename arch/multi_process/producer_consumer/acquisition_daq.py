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
sys.path.insert(1, os.getcwd())

from buffer import DaqBuffer
from acquisition.util.daq_util import extract_channels, extract_devices

from segmentation import SegmentedByTrigger
from acquisition.weigh import Weigh

from arch.multi_process.daq_arch.daq_server import DaqRegister

from mswim.apps.acquisition.models import save_acquisition_data


def memory_usage():
    """
    Return memory usage in MB unity.
    """
    process = psutil.Process(os.getpid())
    return process.get_memory_info()[0] / float(2 ** 20)


def callback_process(group_name, data, sensors_groups):
        # TODO: Re-factor it
        group_channels = sensors_groups['channels']

        temperature_channels = dict(
            [(str(v), i) for i, v in
             sensors_groups['temperature_channels'][0].items()
            ]
        )

        # call the weigh method
        t_0 = time.time()
        #weight = Weigh.calculate({group_name: data})
        print('ok')
        t_1 = time.time()
        print('Weigh Calc Time: %f' % (t_1 - t_0), end=' - ')
        # call the save method
        #save_acquisition_data(data, group_channels, temperature_channels)
        t_2 = time.time()
        print('Save Time: %f' % (t_2 - t_1))
        # call chart method
        # chart.send(data)
        return


def run_server(server):
    return server.read()


def segmentation_check(args):
    client, daq_buffer = args[0], args[1]
    return client.check(daq_buffer)


def segmentation_save(args):
    client, segmented_data = args[0], args[1]
    return client.callback(segmented_data, client.sensors_group)


def loop(servers=[], clients=[], wait=0., daq_buffer=None):
    """
    Loop of routines

    @param routines: List of functions
    @type routines: object
    @param wait: Seconds to wait after each function called
    @type wait: float
    @param daq_buffer: DaqBuffer instance
    @type daq_buffer: DaqBuffer

    """
    print('Starting acquisition.')

    pool = Pool(processes=10)  # start 4 worker processes

    while True:
        if memory_usage() >= 1280:
            raise Exception('Memory usage exceed.')

        time_0 = time.time()

        # Run acquisitions routines
        daq_buffer.append(pool.map(run_server, servers))

        # Look for trigger signal
        indexes = dict(pool.map(
            segmentation_check,
            map(lambda c: (c, daq_buffer.view(c.buffer_name)), clients)
        ))

        # Save segmented data
        if any(indexes.values()):
            clients_filtered = filter(lambda c: indexes[c.buffer_name], clients)
            m = map(
                lambda c: (
                    c,
                    daq_buffer.extract(c.buffer_name, indexes[c.buffer_name])
                ), clients_filtered
            )
            pool.map(segmentation_save, m)

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

    devices = extract_devices(sensors_groups)
    channels = extract_channels(sensors_groups)

    bf = DaqBuffer(channels, samples_per_channel*10)

    for name in devices:
        server.append(DaqRegister(devices[name], samples_per_channel_read))

    """
    # View all signals ring buffer
    chart = DaqPlotter(samples_per_channel=samples_per_channel*2)
    process.append(chart)
    """


    # View only segmented signals
    """
    chart = DaqAsyncPlotter(
        samples_per_channel=samples_per_channel, tree_channels=tree_channels
    )
    client.append(chart)
    """

    def callback_process_in(group_name, data):
        # TODO: Re-factor it
        group_channels = sensors_groups[group_name]['channels']

        temperature_channels = dict(
            [(str(v), i) for i, v in
             sensors_groups[group_name]['temperature_channels'][0].items()
            ]
        )


        # call the weigh method
        t_0 = time.time()
        weight = Weigh.calculate({group_name: data})
        t_1 = time.time()
        print('Weigh Calc Time: %f' % (t_1 - t_0), end=' - ')
        # call the save method
        save_acquisition_data(data, group_channels, temperature_channels)
        t_2 = time.time()
        print('Save Time: %f' % (t_2 - t_1))
        # call chart method
        # chart.send(data)
        return

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
                callback=callback_process,
                sensors_group=sensors_groups[name]
            )
        )

    try:
        loop(
            servers=server,
            clients=client,
            wait=0.0001,
            daq_buffer=bf
        )
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
