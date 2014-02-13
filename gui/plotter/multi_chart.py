from __future__ import division, print_function
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter

import numpy as np


def start():
    plt.ion()
    plt.show()


def stop():
    plt.ioff()


def plotter(data_size=100, wait=0.00001):
    start()

    time = np.arange(0, 1, 1/data_size)
    formatter = EngFormatter(unit='s', places=1)
    # interval
    frame_limits = [0, 1, -10, 10]

    while True:
        data = (yield)

        chart_n = len(data.keys())

        if not chart_n:
            continue

        plt.clf()

        i = 0
        for name in data:
            i += 1
            chart_id = chart_n*100 + 10 + i
            for ch in data[name]:
                ax = plt.subplot(chart_id)
                ax.xaxis.set_major_formatter(formatter)
                ax.axis(frame_limits)
                ax.grid()
                ax.set_xlabel(name)
                ax.plot(time, data[name][ch])

        plt.draw()
        plt.pause(wait)


if __name__ == '__main__':
    def main():
        data_size = 100
        mplt = plotter(data_size=data_size, wait=0.00001)
        mplt.next()

        a = -8
        b = +8

        while True:
            data = {
                'Dev1': (b - a) * np.random.random_sample((data_size,)) + a,
                'Dev2': (b - a) * np.random.random_sample((data_size,)) + a,
                'Dev3': (b - a) * np.random.random_sample((data_size,)) + a
            }
            mplt.send(data)

        stop()

    try:
        main()
    except:
        stop()
        print('Exit.')