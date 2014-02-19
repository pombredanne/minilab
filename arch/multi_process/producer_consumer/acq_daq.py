# -*- coding: utf-8 -*-
"""
Consumer and Producer structure

"""
from __future__ import print_function, division

import multiprocessing
import os
import sys

from multiprocessing import Pool

import server

from buffer import DaqBuffer
from server import DaqRegister
from plotter import PlotTask

sys.path.insert(0, '/var/www/mswim/')
sys.path.insert(1, os.getcwd())

from acquisition.util.daq_util import (
    extract_all_channels, extract_channels, extract_devices
)

from save import save_acquisition_data
from segmentation import SegmentTask


class Consumer(multiprocessing.Process):
    """

    """
    def __init__(
        self, device_settings, task_queue, result_queue, samples_per_channel
    ):
        multiprocessing.Process.__init__(self)

        self.name = device_settings.keys()[0]

        self._task_queue = task_queue
        self._result_queue = result_queue

        self._daq = DaqRegister(
            device=device_settings.values()[0],
            samples_per_channel=samples_per_channel
        )

    def run(self):
        print(id(self))
        while True:
            self._task_queue.get()

            """
            if bf is None:
                self._task_queue.task_done()
                break
            """

            self._task_queue.task_done()
            self._result_queue.put([self._daq.read()])

        return


def start_acquisition(sensors_settings, dsn):
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    devices = extract_devices(sensors_settings)
    all_channels = extract_all_channels(sensors_settings)
    channels = extract_channels(sensors_settings)

    pool = Pool(processes=4)

    chunk = 15000

    segmented_task = SegmentTask(
        chunk=chunk,
        sensors=sensors_settings
    )

    daq_buffer = DaqBuffer(
        sensors_groups=all_channels,
        limit_per_channel=chunk*100
    )

    plot_task = PlotTask(
        channels=sensors_settings,
        data_size=chunk
    )

    consumers = [
        Consumer(i, tasks, results, chunk)
        for i in [{k: v} for k, v in devices.items()]
    ]

    process_n = len(consumers)

    for w in consumers:
        w.start()

    # loop
    while True:
        for _ in range(process_n):
            tasks.put(True)
            daq_buffer.append(results.get())

        segmented_data = segmented_task(daq_buffer)

        if segmented_data:
            """
            data={}, channels=[], sensors_settings={},
            weight_data={}, dsn='', schema=''
            """
            pool.apply_async(
                save_acquisition_data,
                args=(
                    segmented_data, channels, sensors_settings,
                    {}, dsn, 'mswim'
                )
            )
            plot_task.plot(segmented_data)


if __name__ == '__main__':
    # internal
    sys.path.append('/var/www/mswim/')

    from mswim.settings import DEVICES as SENSORS_GROUP
    from mswim.libs.db import conn
    from mswim import settings

    # REMOVE GROUPS WITH ACQUISITION EQUAL TO FALSE
    _sensors_settings = {}
    for i in SENSORS_GROUP:
        if SENSORS_GROUP[i]['acquisition_mode']:
            _sensors_settings[i] = SENSORS_GROUP[i]

    start_acquisition(_sensors_settings, conn.Pool.dsn(settings))