from __future__ import print_function, division
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from random import random, randint
from copy import deepcopy

import time
import numpy as np
import traceback

class DaqMultiPlotter(object):
    """

    """
    data_size = None
    time = None
    formatter = EngFormatter(unit='s', places=1)
    data = {}

    # interval
    frame_limits = None

    @classmethod
    def configure(cls, samples_per_channel, devices=[]):
        """

        """
        cls.data_size = samples_per_channel
        cls.time = np.linspace(0, 1, samples_per_channel)
        cls.formatter = EngFormatter(unit='s', places=1)

        # interval
        cls.frame_limits = [0, 1, -10, 10]

        for dev in devices:
            cls.data[dev] = {}

    @classmethod
    def start(cls):
        plt.ion()
        plt.show()

    @classmethod
    def send_data(cls, data):
        """

        """
        for buffer_name, buffer_data in data.items():
            cls.data[buffer_name] = buffer_data

    @classmethod
    def show(cls):
        plt.clf()
        num_charts = len(cls.data)
        i = 0

        buffer_data = deepcopy(cls.data)

        for buffer_name in buffer_data:
            i += 1
            chart_id = num_charts*100 + 10 + i

            ax = plt.subplot(chart_id)
            ax.xaxis.set_major_formatter(cls.formatter)
            ax.set_xlabel(buffer_name)
            ax.axis(cls.frame_limits)
            ax.set_autoscale_on(False)
            plt.grid()
            for ch, ch_data in buffer_data[buffer_name].items():
                if len(cls.time) != len(ch_data):
                    print(len(cls.time), len(ch_data), ch)
                ax.plot(cls.time, ch_data)

        plt.draw()
        plt.pause(0.00000001)

    @classmethod
    def stop(cls):
        plt.ioff()
        plt.show()


if __name__ == '__main__':
    def test1():
        """

        """
        cols = 2
        rows = 1000
        num_frames = 100
        interval_a = -8
        interval_b = +8

        data = defaultdict(dict)

        DaqMultiPlotter.configure(rows, ['ceramic', 'polymer'])

        DaqMultiPlotter.start()

        try:
            while True:
                for group in ['ceramic', 'polymer']:
                    for x in range(cols):
                        data[group]['Dev1/ia%s' % x] = (
                            (interval_b - interval_a) *
                            np.random.random_sample((rows,)) + interval_a
                        )
                DaqMultiPlotter.send_data(data)
        except Exception as e:
            print(traceback.format_exc())

        DaqMultiPlotter.stop()

    test1()
    # math_algorithms