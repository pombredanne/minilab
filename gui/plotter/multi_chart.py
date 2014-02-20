from __future__ import division, print_function
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter

import numpy as np
import time


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
            ax = plt.subplot(chart_n*100 + 10 + i)
            ax.grid()
            ax.set_xlabel(name)
            ax.xaxis.set_major_formatter(formatter)
            ax.axis(frame_limits)
            for ch in data[name]:
                ax.plot(time, data[name][ch])

        plt.draw()
        plt.pause(wait)


if __name__ == '__main__':
    def main():
        data_size = 1000
        mplt = plotter(data_size=data_size, wait=0.00001)
        mplt.next()

        a = -8
        b = +8

        while True:
            data = {
                'Dev1': {
                    'Dev1/ai1': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev1/ai2': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev1/ai3': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev1/ai4': (b - a) * np.random.random_sample((data_size,)) + a
                },
                'Dev2': {
                    'Dev2/ai1': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev2/ai2': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev2/ai3': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev2/ai4': (b - a) * np.random.random_sample((data_size,)) + a
                },
                'Dev3': {
                    'Dev3/ai1': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev3/ai2': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev3/ai3': (b - a) * np.random.random_sample((data_size,)) + a,
                    'Dev3/ai4': (b - a) * np.random.random_sample((data_size,)) + a
                }
            }
            time_0 = time.time()
            mplt.send(data)
            print('%f' % (time.time() - time_0))

        stop()

    try:
        main()
    except Exception as e:
        stop()
        print(e.message)
        print('Exit.')