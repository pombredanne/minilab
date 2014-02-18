from __future__ import print_function, division
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter

import numpy as np


class PlotTask(object):
    data_buffer = {}

    def __init__(self, channels={}, data_size=1):
        self.data_size = data_size
        self.time = np.arange(0, 1, 1/data_size)
        self.formatter = EngFormatter(unit='s', places=1)

        self.frame_limits = [0, 1, -10, 10]
        self.chart_n = len(channels.keys())

        for grp_name, grp_channels in channels.items():
            # prepare channel data
            chs = dict(
                (v, k) for z in grp_channels['channels'] for v, k in z.items()
            )

            self.data_buffer[grp_name] = dict(
                (ch_name, [0]*self.data_size)
                for ch_name in chs
            )

        plt.ion()
        plt.show()

    def plot(self, data={}):
        plt.clf()

        i = 0
        for group_name in self.data_buffer:
            if not group_name in data:
                continue

            self.data_buffer[group_name] = data[group_name]
            i += 1
            chart_id = self.chart_n*100 + 10 + i
            for ch_name, ch_data in data[group_name].items():
                ax = plt.subplot(chart_id)
                ax.xaxis.set_major_formatter(self.formatter)
                ax.axis(self.frame_limits)
                ax.grid()
                ax.set_xlabel(group_name)

                if not len(ch_data):
                    ch_data = [0]*len(self.time)
                    print(ch_name, 'NULL DATA')

                ax.plot(self.time, ch_data)
        plt.grid()
        plt.draw()
        plt.pause(0.000000001)
        return True

    def __del__(self):
        plt.ioff()