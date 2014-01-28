from __future__ import print_function, division
from pylab import *
from random import random
import time
import numpy as np


def plt_start(number_of_lines):
    ion()

    lines = []
    for _ in xrange(number_of_lines):
        line, = plot(arange(0, 0.01*100, 0.01), [0]*100)
        lines.append(line)
    return lines


def plt_plotter(data, lines):
    """

    """
    for i in range(1, int(1000/100)):
        for key, line in enumerate(lines):
            sensors = data[key]

            frame = sensors[i*100:(i+1)*100]
            line.set_ydata(frame)  # update the data
            draw()                 # redraw the canvas
            pause(0.0000000001)


def plt_stop():
    ioff()
    show()

if __name__ == '__main__':
    line = plt_start()

    data = []
    cols = 16
    rows = 1000

    for x in range(cols):
        data.append([random() for _ in range(rows)])

    plt_plotter(data, line)

    for x in range(cols):
        data.append([-random() for _ in range(rows)])

    plt_plotter(data, line)

    plt_stop()