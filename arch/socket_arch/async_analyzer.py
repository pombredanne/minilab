from __future__ import print_function, division
from collections import defaultdict
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from random import random, randint

import time
import numpy as np


class DaqMultiPlotter():
    """

    """
    data_size = None
    time = None
    formatter = EngFormatter(unit='s', places=1)

    # interval
    frame_limits = None

    @classmethod
    def configure(cls, samples_per_channel):
        """

        """
        cls.data_size = samples_per_channel
        cls.time = np.linspace(0, 1, samples_per_channel)
        cls.formatter = EngFormatter(unit='s', places=1)

        # interval
        cls.frame_limits = [0, 1, -10, 10]

    @classmethod
    def start(cls):
        plt.ion()
        plt.show()

    @classmethod
    def send_data(cls, data):
        """

        """
        plt.clf()

        num_charts = len(data)
        i = 0
        for buffer_name in data:
            i += 1
            chart_id = num_charts*100 + 10 + i
            for channel in data[buffer_name]:
                ax = plt.subplot(chart_id)
                ax.xaxis.set_major_formatter(cls.formatter)
                ax.grid()

                ax.plot(cls.time, data[buffer_name][channel])

        plt.draw()
        plt.pause(0.000001)

    @classmethod
    def stop(cls):
        plt.ioff()
        plt.show()


if __name__ == '__main__':
    def test1():
        """

        """
        cols = 16
        rows = 1000
        num_frames = 100
        interval_a = -8
        interval_b = +8

        data = defaultdict(dict)

        DaqMultiPlotter.configure(rows)

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
        except:
            pass

        DaqMultiPlotter.stop()

    test1()
    # math_algorithms