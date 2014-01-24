from pylab import *
from random import random
import time
import numpy as np


def plt_start():
    ion()
    line, = plot(arange(0, 0.01*100, 0.01), [0]*100)
    return line


def plt_plotter(data, line):
    """

    """
    tstart = time.time()               # for profiling

    data = data[0]

    for i in range(1, 1000/100):
        frame = data[i*100:(i+1)*100]
        line.set_ydata(frame)  # update the data
        draw()                 # redraw the canvas
        pause(0.02)


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