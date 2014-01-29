# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""
from __future__ import print_function
from PyDAQmx import *
from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *

import numpy as np


class AnalogContinuousTask():
    """

    """
    task = None
    physical_channel = None
    seconds_to_acquire = None
    rate = None
    samples_per_channel = None
    number_of_channels = None
    buffer_size = None
    minv = None
    maxv = None

    def __init__(
        self,
        physical_channel=[],
        rate=1.0,
        minv=(-5.0),
        maxv=5.0,
        seconds_to_acquire=3
    ):
        """

        """
        self.task = TaskHandle()
        self.physical_channel = physical_channel
        self.seconds_to_acquire = seconds_to_acquire
        self.rate = rate

        self.samples_per_channel = int(self.rate * 1)  # 1 second sampled
        self.number_of_channels = len(physical_channel)
        self.buffer_size = self.samples_per_channel * self.number_of_channels

        self.minv = minv
        self.maxv = maxv

        DAQmxCreateTask('', byref(self.task))

        DAQmxCreateAIVoltageChan(
            self.task,
            ','.join(self.physical_channel),
            '',
            DAQmx_Val_RSE,
            self.minv,
            self.maxv,
            DAQmx_Val_Volts,
            None
        )

        # note: Finite time raise -200284 error
        DAQmxCfgSampClkTiming(
            self.task,
            '',
            self.rate,
            DAQmx_Val_Rising,
            DAQmx_Val_ContSamps,
            self.samples_per_channel
        )

        DAQmxStartTask(self.task)


    def read(self):
        """
        @return: data acquisitions, time of each acquisition
        """
        data = self._read()

        return dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channel)
        ])

    def _read(self):
        """

        """
        data = np.zeros((self.buffer_size,), dtype=numpy.float64)
        read = int32()

        DAQmxReadAnalogF64(
            self.task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.buffer_size,
            byref(read),
            None
        )

        return data

    def close(self):
        print('')
        print('Clearing ...')
        try:
            DAQmxStopTask(self.task)
            print('\nTask stopped')
        except:
            pass

        try:
            DAQmxClearTask(self.task)
            print('Quit')
        except:
            pass
        return

class DigitalContinuousTask(object):
    """

    """
    task = None
    channels = None
    read_int32 = None
    bytes_per_samp_int32 = None
    samples_per_channel = None

    def __init__(
        self,
        channels,
        samples_per_channel
    ):
        self.task = TaskHandle()
        self.channels = channels
        self.samples_per_channel = samples_per_channel
        self.read_int32 = int32()
        self.bytes_per_samp_int32 = int32()

    def read(self):
        """

        """
        data = numpy.zeros((self.samples_per_channel,), dtype=numpy.uint8)

        DAQmxCreateTask("", byref(self.task))
        DAQmxCreateDIChan(
            self.task,
            ','.join(self.channels),
            '',
            DAQmx_Val_ChanPerLine
        )

        DAQmxStartTask(self.task)

        DAQmxReadDigitalLines(
            self.task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.samples_per_channel * 2,
            byref(self.read_int32),
            byref(self.bytes_per_samp_int32),
            None
        )

        return data

    def close(self):
        """

        @return:

        """
        print('')
        print('Clearing ...')
        try:
            DAQmxStopTask(self.task)
            print('\nTask stopped')
        except:
            pass

        try:
            DAQmxClearTask(self.task)
            print('Quit')
        except:
            pass
        return


