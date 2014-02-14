from __future__ import generators, print_function
from multiprocessing import Pool
from collections import defaultdict

import sys
import time
import os
import numpy as np
import psutil
from copy import deepcopy
# internal
#sys.path.append('../../..')
from gui.plotter.multi_chart import plotter


def memory_usage():
    """
    Return memory usage in MB unity.
    """
    process = psutil.Process(os.getpid())
    return process.get_memory_info()[0]/float(2**20)


class BufferRing(object):
    """

    """
    data_buffer = defaultdict(dict)

    def append(self, data):
        """
        Append data to buffer

        """
        for buffer_name in data:
            for ch in data[buffer_name]:
                if not ch in self.data_buffer[buffer_name]:
                    self.data_buffer[buffer_name][ch] = []
                self.data_buffer[buffer_name][ch] += data[buffer_name][ch]

    def extract(self, callback=None):
        """
        Extract data from buffer

        """
        data = defaultdict(dict)

        for name in self.data_buffer:
            for ch in self.data_buffer[name]:
                if len(self.data_buffer[name][ch]) < 1000:
                    data[name][ch] = [0] * 1000
                else:
                    data[name][ch] = self.data_buffer[name][ch][:1000]
                    self.data_buffer[name][ch][:] = (
                        self.data_buffer[name][ch][1000:]
                    )
        return data


def process_daq(daq):
    return daq.read()


class DAQ(object):
    """

    """
    def __init__(self, name):
        self.name = name

    def read(self, *args):
        """

        """
        result = {}
        for i in xrange(32):
            result[i] = list(np.random.random(1000))

        return self.name, result


if __name__ == "__main__":
    threads = []

    bf = BufferRing()

    threads.append(DAQ('Dev1'))
    threads.append(DAQ('Dev2'))
    threads.append(DAQ('Dev4'))
    threads.append(DAQ('Dev5'))

    mplt = plotter(data_size=1000)
    mplt.next()

    pool = Pool(processes=4)  # start 4 worker processes
    pool2 = Pool(processes=1)  # start 4 worker processes

    while True:
        if memory_usage() > 1280:
            raise Exception('Memory usage exceed 1GB.')

        time_0 = time.time()
        data = dict(pool.map(process_daq, threads))
        time_1 = time.time()
        print('%f' % (time_1 - time_0), end=' - ')
        bf.append(data)
        mplt.send(bf.extract())
        print('%f' % (time.time() - time_1), end=' - ')
        print('%f' % (time.time() - time_0))
