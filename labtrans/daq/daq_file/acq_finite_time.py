# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""
from __future__ import print_function, division
from PyDAQmx import *
from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
from matplotlib import pyplot as plt

import numpy as np
import time


class AcquisitionFiniteTask():
    """

    """

    def __init__(self, physical_channel=[], rate=1.0, minv=-5.0, maxv=5.0, time_to_acquire=2):
        """

        """
        self.task = TaskHandle()
        self.physical_channel = physical_channel
        self.time_to_acquire = time_to_acquire
        self.rate = rate
        self.samples_per_channel = int(self.rate * self.time_to_acquire)
        self.number_of_channels = len(physical_channel)
        self.buffer_size = self.samples_per_channel * self.number_of_channels

        self.minv = minv
        self.maxv = maxv

        DAQmxCreateTask('AcquisitionFiniteTask', byref(self.task))

        DAQmxCreateAIVoltageChan(
            self.task, ','.join(self.physical_channel), "",
            DAQmx_Val_RSE, self.minv, self.maxv,
            DAQmx_Val_Volts, None
        )

        # note: Finite time raise -200284 error
        DAQmxCfgSampClkTiming(
            self.task, '', self.rate, DAQmx_Val_Rising,
            DAQmx_Val_ContSamps, self.samples_per_channel
        )

    def read(self):
        data = self._read()

        return dict([
            (name, data[i*self.samples_per_channel:(i+1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channel)
        ])

    def _read(self):
        DAQmxStartTask(self.task)
        data = np.zeros(
            self.buffer_size,
            dtype=np.float64
        )

        # data = AI_data_type()
        read = int32()
        DAQmxReadAnalogF64(
            self.task, self.samples_per_channel, 10.0,
            DAQmx_Val_GroupByChannel, data,
            self.buffer_size, byref(read), None
        )

        #DAQmxWaitUntilTaskDone(self.task, 10.0)  # only for FiniteSamps mode
        DAQmxStopTask(self.task)
        DAQmxClearTask(self.task)

        return data

    def plot(self, data):
        plt.axis([0, self.samples_per_channel-1, -11, 11])

        for line in data:
            #plt.plot(data['Dev2/ai3'])
            plt.plot(data[line])

        plt.grid()
        plt.show()
