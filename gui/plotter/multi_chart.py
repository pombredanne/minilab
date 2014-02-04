from __future__ import division, print_function
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter

import numpy as np

plt.ion()
plt.show()

data_size = 100
time = np.arange(0, 1, 1/data_size)
formatter = EngFormatter(unit='s', places=1)
# interval
a = -8
b = +8
frame_limits = [0, 1, -10, 10]
while True:
    plt.clf()

    for _ in range(5):
        ax = plt.subplot(311)
        ax.xaxis.set_major_formatter(formatter)
        ax.axis(frame_limits)
        data = (b - a) * np.random.random_sample((data_size,)) + a
        ax.grid()
        ax.plot(time, data)

    for _ in range(5):
        ax = plt.subplot(312)
        ax.xaxis.set_major_formatter(formatter)
        ax.axis(frame_limits)
        ax.grid()
        data = (b - a) * np.random.random_sample((data_size,)) + a
        ax.plot(time, data)

    for _ in range(5):
        ax = plt.subplot(313)
        ax.xaxis.set_major_formatter(formatter)
        ax.axis(frame_limits)
        ax.grid()
        data = (b - a) * np.random.random_sample((data_size,)) + a
        ax.plot(time, data)

    plt.draw()
    plt.pause(0.00001)