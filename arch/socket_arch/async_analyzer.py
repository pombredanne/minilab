from __future__ import print_function, division
from collections import defaultdict
from pylab import ion, ioff, plot, arange, draw, pause, show
from random import random, randint

import pylab
import time
import numpy as np


def plt_start(number_of_chart_lines):
    ion()
    pylab.grid()

    lines = []
    for _ in xrange(number_of_chart_lines):
        line, = plot(arange(0, 0.01*100, 0.01), [0]*100)
        lines.append(line)
    return lines


def plt_plotter(data, chart_lines, name='ceramic'):
    """

    """
    for i in range(1, int(1000/100)):
        for key_line, line in enumerate(chart_lines):
            sensors = data[data.keys()[key_line]]
            print(sensors)

            frame = sensors[i*100:(i+1)*100]
            line.set_ydata(frame)  # update the data
            draw()                 # redraw the canvas
            pause(0.0000000001)


def plt_stop():
    ioff()
    show()


if __name__ == '__main__':
    def test():
        data = defaultdict(list)
        cols = 16
        rows = 1000

        chart_lines = plt_start(cols)

        for x in range(cols):
            data['Dev1/ia%s' % x].append([random() for _ in range(rows)])

        plt_plotter(data, chart_lines)

        plt_stop()

    test()