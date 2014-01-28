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
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np
import random


from mswim.apps.acquisition.models import AcquisitionModel


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
        self.samples_per_channel = int(self.rate * self.seconds_to_acquire)
        self.number_of_channels = len(physical_channel)
        self.buffer_size = self.samples_per_channel * self.number_of_channels

        self.minv = minv
        self.maxv = maxv

        DAQmxCreateTask('AcquisitionFiniteTask', byref(self.task))

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


    def read(self):
        """
        @return: data acquisitions, time of each acquisition
        """
        data = self._read()

        return dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channel)
        ]), calc_time(timedelta(1 / self.rate), self.samples_per_channel)


    def _read(self):
        DAQmxStartTask(self.task)
        data = np.zeros(
            self.buffer_size,
            dtype=np.float64
        )

        # data = AI_data_type()
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

        # DAQmxWaitUntilTaskDone(self.task, 10.0)  # only for FiniteSamps mode
        DAQmxStopTask(self.task)
        # DAQmxClearTask(self.task)

        return data


class DigitalContinuousTask(object):
    """

    """
    digital_task = None
    channels = None
    read_int32 = None
    bytes_per_samp_int32 = None
    samples_per_channel = None

    def __init__(
        self,
        channels,
        samples_per_channel
    ):
        self.digital_task = TaskHandle()
        self.channels = channels
        self.samples_per_channel = samples_per_channel
        self.read_int32 = int32()
        self.bytes_per_samp_int32 = int32()

    def read(self):
        """

        """
        data = numpy.zeros((self.samples_per_channel,), dtype=numpy.uint8)

        DAQmxCreateTask("", byref(self.digital_task))
        DAQmxCreateDIChan(
            self.digital_task,
            ','.join(self.channels),
            '',
            DAQmx_Val_ChanPerLine
        )

        DAQmxStartTask(self.digital_task)

        DAQmxReadDigitalLines(
            self.digital_task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.samples_per_channel * 2,
            byref(self.read_int32),
            byref(self.bytes_per_samp_int32),
            None
        )

        DAQmxStopTask(self.digital_task)
        DAQmxClearTask(self.digital_task)

        return data

    def clear(self):
        """

        @return:

        """
        print('')
        print('Clearing ...')
        try:
            DAQmxStopTask(self.digital_task)
            print('\nTask stopped')
        except:
            pass

        try:
            DAQmxClearTask(self.digital_task)
            print('Quit')
        except:
            pass
        return


