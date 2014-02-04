# -*- coding: utf-8 -*-
"""


"""
from matplotlib import pyplot
from matplotlib.ticker import EngFormatter

import numpy as np


def multi_sin(channels, samples_per_channel):
    t = np.linspace(-1, 1, samples_per_channel)
    yield t

    data_size = t.size

    result = {}
    while True:
        for position in xrange(0, samples_per_channel, 100):
            result.clear()
            for k, ch in enumerate(channels):
                data = list(t[position:data_size]) + list(t[0:position])
                data = np.sin(2 * np.pi * np.array(data) + k) * 10

                result[ch] = data

            yield result


def show(t):
    pyplot.ion()
    pyplot.show()

    formatter = EngFormatter(unit='s', places=1)

    while True:
        data = yield

        pyplot.clf()

        for ch in data:
            ax = pyplot.subplot(111)
            ax.xaxis.set_major_formatter(formatter)
            ax.grid()
            ax.plot(t, data[ch])

        pyplot.grid()
        pyplot.draw()
        pyplot.pause(0.00000000000000001)

    pyplot.ioff()

if __name__ == '__main__':
    def test1():
        """

        """
        samples_per_channel = 1000
        func = multi_sin(
            channels=['Dev1/ai%s' % i for i in range(16)],
            samples_per_channel=samples_per_channel
        )
        t = func.next()

        chart = show(t)
        chart.next()

        while True:
            data = func.next()
            chart.send(data)

    test1()