"""
Consumer and Producer structure

"""
from __future__ import print_function, division
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from time import sleep

import random
import numpy as np

import multiprocessing


class DAQ(object):
    population = range(10)*3

    def __init__(self, device_settings):
        self.name = device_settings.keys()[0]
        self.channels = device_settings[self.name]['channels']
        self.trigger = device_settings[self.name]['trigger']

    def listening_device(self):
        return {
            self.name: dict(
                (ch, random.sample(self.population, 10))
                for ch in self.channels + [self.trigger]
            )
        }


class Consumer(multiprocessing.Process):
    """

    """
    def __init__(self, device_settings, task_queue, result_queue):
        multiprocessing.Process.__init__(self)

        self.name = device_settings.keys()[0]

        self._task_queue = task_queue
        self._result_queue = result_queue
        self._daq = DAQ(device_settings)

    def run(self):
        print(id(self))
        while True:
            segmented_task, bf = self._task_queue.get()

            if segmented_task is None:
                self._task_queue.task_done()
                break

            bf.append(self._daq.listening_device())
            segmented_data = segmented_task(
                daq_buffer=bf, daq=self._daq
            )

            self._task_queue.task_done()
            self._result_queue.put((self._daq.name, segmented_data))

        return


class DaqBuffer(object):
    data = defaultdict(dict)
    max_size_buffer = None

    def __init__(self, max_size_buffer):
        self.max_size_buffer = max_size_buffer

    def append(self, data):
        for group_name, _data in data.items():
            for ch, ch_data in _data.items():
                if not ch in self.data[group_name]:
                    self.data[group_name][ch] = []
                self.data[group_name][ch][:] += ch_data

    def extract(self, group_name, start, end):
        """

        """
        result = {}
        for ch, ch_data in self.data[group_name].items():
            result[ch] = ch_data[start: end]
            ch_data[:] = ch_data[end:]
        return result

    def view(self, group_name):
        """

        """
        result = {}
        for ch, ch_data in self.data[group_name].items():
            result[ch] = ch_data
        return result


class SegmentTask(object):
    chunk = None

    def __init__(self, chunk=0):
        self.chunk = chunk

    def __call__(self, daq_buffer, daq):
        trigger_data = daq_buffer.view(daq.name)[daq.trigger]

        data_size = len(trigger_data)

        try:
            i = trigger_data.index(1)
        except ValueError:
            return None

        if i + self.chunk > data_size:
            return None

        return daq_buffer.extract(daq.name, i, i+self.chunk)


class PlotTask(object):
    data_buffer = {}

    def __init__(self, channels={}, data_size=1):
        self.data_size = data_size
        self.time = np.arange(0, 1, 1/data_size)
        self.formatter = EngFormatter(unit='s', places=1)

        self.frame_limits = [0, 1, -10, 10]
        self.chart_n = len(channels.keys())

        for grp_name, grp_channels in channels.items():
            self.data_buffer[grp_name] = dict(
                (ch_name, [0]*self.data_size)
                for ch_name in grp_channels
            )

        plt.ion()
        plt.show()

    def plot(self, group_name, data):
        plt.clf()

        self.data_buffer[group_name] = data
        i = 0
        for grp_name, grp_data in self.data_buffer.items():
            i += 1
            chart_id = self.chart_n*100 + 10 + i
            for ch_name, ch_data in grp_data.items():
                ax = plt.subplot(chart_id)
                ax.xaxis.set_major_formatter(self.formatter)
                ax.axis(self.frame_limits)
                ax.grid()
                ax.set_xlabel(grp_name)

                ax.plot(self.time, ch_data)
        plt.grid()
        plt.draw()
        plt.pause(0.000000001)
        return True

    def __del__(self):
        plt.ioff()


def start_acquisition():
    tasks = multiprocessing.JoinableQueue()
    results = multiprocessing.Queue()

    channels = {
        'Dev1': {
            'channels': ['Dev1/ai%s' % ch for ch in range(2)],
            'trigger': 'Dev1/di0'},
        'Dev2': {
            'channels': ['Dev2/ai%s' % ch for ch in range(2)],
            'trigger': 'Dev2/di0'}
    }

    chunk = 1000

    seg_task = SegmentTask(chunk=chunk)
    daq_buffer = DaqBuffer(max_size_buffer=chunk*100)
    plot_task = PlotTask(
        channels=channels,
        data_size=chunk
    )

    consumers = [
        Consumer(i, tasks, results)
        for i in [{k: v} for k, v in channels.items()]
    ]

    for w in consumers:
        w.start()

    # loop
    while True:
        tasks.put((seg_task, daq_buffer))
        daq_name, segmented_data = results.get()

        if segmented_data:
            plot_task.plot(daq_name, segmented_data)


if __name__ == '__main__':
    start_acquisition()