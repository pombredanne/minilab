from __future__ import division, print_function
from matplotlib import pyplot
from matplotlib.ticker import EngFormatter

import numpy as np


def sin_wave(channels, samples_per_channel):
    t = np.linspace(-1, 1, samples_per_channel)
    yield t

    data_size = t.size

    result = {}
    while True:
        for position in xrange(0, samples_per_channel, 100):
            result.clear()
            for k, ch in enumerate(channels.values()[0]):
                data = list(t[position:data_size]) + list(t[0:position])
                data = np.sin(2 * np.pi * np.array(data) + k) * 10

                result[ch] = data

            yield result


def triangle_wave(channels, samples_per_channel):
    t = np.linspace(-8, 8, samples_per_channel)
    number_of_channels = len(channels.values()[0])

    yield t

    data_size = t.size
    amplitude = 5

    result = {}
    while True:
        for position in xrange(0, samples_per_channel, 10):
            result.clear()
            for k, ch in enumerate(channels.values()[0]):
                data = list(t[position:data_size]) + list(t[0:position])
                data = np.array(data) + (k / number_of_channels) * amplitude

                result[ch] = data

            yield result


def show(channels, t):
    pyplot.ion()
    pyplot.show()

    formatter = EngFormatter(unit='s', places=1)
    frame_limits = [0, 1, -11, 11]

    while True:
        data = yield

        pyplot.clf()

        for ch in data:
            ax = pyplot.subplot(111)
            ax.xaxis.set_major_formatter(formatter)
            ax.set_xlabel(channels.keys()[0])
            ax.axis(frame_limits)
            ax.set_autoscale_on(False)
            ax.plot(t, data[ch])
        pyplot.grid()
        pyplot.draw()
        pyplot.pause(0.000000000001)

    pyplot.ioff()

if __name__ == '__main__':
    def test1():
        """

        """
        samples_per_channel = 1000
        channels = {'Dev1': ['Dev1/ai%s' % i for i in range(2)]}
        wave_function = triangle_wave(
            channels=channels,
            samples_per_channel=samples_per_channel
        )
        t = wave_function.next()

        chart = show(channels, t)
        chart.next()

        while True:
            data = wave_function.next()
            len(data)
            chart.send(data)

    test1()