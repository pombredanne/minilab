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
    physical_channels = None
    seconds_to_acquire = None
    rate = None
    samples_per_channel = None
    number_of_channels = None
    buffer_size = None
    buffer_daq_size = None
    minv = None
    maxv = None

    def __init__(
        self,
        physical_channels=[],
        rate=1000.,
        minv=(-5.0),
        maxv=5.0,
        seconds_to_acquire=3,
        samples_per_channel=1000
    ):
        """

        """
        self.task = TaskHandle()
        self.physical_channels = physical_channels
        self.seconds_to_acquire = seconds_to_acquire
        self.rate = rate

        self.samples_per_channel = samples_per_channel
        self.number_of_channels = len(physical_channels)
        self.buffer_size = self.samples_per_channel * self.number_of_channels
        self.buffer_daq_size = self.buffer_size * self.rate/4  # w/ calibration

        self.minv = minv
        self.maxv = maxv

        DAQmxCreateTask('', byref(self.task))

        DAQmxCreateAIVoltageChan(
            self.task,
            ','.join(self.physical_channels),
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
            self.buffer_daq_size
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
            for i, name in enumerate(self.physical_channels)
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
    physical_channels = None
    read_int32 = None
    bytes_per_samp_int32 = None
    samples_per_channel = None
    buffer_size = None
    buffer_daq_size = None

    def __init__(
        self,
        physical_channels=[],
        rate=1000.,
        samples_per_channel=1000
    ):
        self.task = TaskHandle()
        self.physical_channels = physical_channels
        self.rate = rate
        self.samples_per_channel = samples_per_channel
        self.buffer_size = self.samples_per_channel * len(physical_channels)
        self.buffer_daq_size = self.buffer_size * self.rate/4  # w/ calibration

        if physical_channels:
            DAQmxCreateTask("", byref(self.task))
            DAQmxCreateDIChan(
                self.task,
                ','.join(self.physical_channels),
                '',
                DAQmx_Val_ChanPerLine
            )

    def read(self):
        """
        @return: data acquisitions, time of each acquisition
        """
        if not self.physical_channels:
            return {}

        data = self._read()

        result = dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channels)
        ])
        return result

    def _read(self):
        """

        """
        data = numpy.zeros((self.samples_per_channel,), dtype=numpy.uint8)
        samps_per_chan_read_i = int32()
        bytes_per_samp_i = int32()

        DAQmxStartTask(self.task)

        DAQmxReadDigitalLines(
            self.task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.samples_per_channel,
            byref(samps_per_chan_read_i),
            byref(bytes_per_samp_i),
            None
        )

        DAQmxStopTask(self.task)

        return data

    def close(self):
        """

        @return:

        """
        if not self.physical_channels:
            return

        print('\nStopping ... ', end='')
        try:
            DAQmxStopTask(self.task)
        except:
            pass

        try:
            DAQmxClearTask(self.task)
        except:
            pass

        print('OK. Quit.')
        return


if __name__ == '__main__':
    import sys
    import platform

    # internal
    sys.path.append('../../')
    from arch.socket_arch.util import extract_devices

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim.settings import DEVICES

    device = extract_devices(DEVICES)['Dev5']
    digital_task = DigitalContinuousTask(
        physical_channels=device['digital'],
        rate=device['rate']
    )

    print(digital_task.read())