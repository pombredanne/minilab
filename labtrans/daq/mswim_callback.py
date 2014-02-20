# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:04:42 2013

@author: ivan
"""
from __future__ import division, print_function
from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from numpy import zeros, linspace
from datetime import datetime, timedelta
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter

import time

"""This example is a PyDAQmx version of the ContAcq_IntClk.c example
It illustrates the use of callback function

This example demonstrates how to acquire a continuous amount of
data using the DAQ device's internal clock. It incrementally store the data
in a Python list.

This example is also an example for the object oriented uses of PyDAQmx
"""


def calc_time(delta_t, N):
    _ts = datetime.now()

    def nexttime(_ts):
        _timestamp = _ts
        _ts += delta_t
        return _timestamp

    return [nexttime(_ts) for _ in range(N)]


class AcquisitionCallbackTask(Task):
    """

    """

    def __init__(
            self, physicalChannel=[], rate=1.0, minv=-5.0, maxv=5.0,
            digitalChannel=None
    ):
        """

        """
        Task.__init__(self)

        self.device_name = physicalChannel[0].split('/')[0]

        self.rate = rate
        self.minv = minv
        self.maxv = maxv
        self.samplesPerChannel = int(rate)

        self.bufferSize = len(physicalChannel) * self.samplesPerChannel
        self.numberOfChannel = physicalChannel.__len__()

        if type(physicalChannel) == type(""):
            self.physicalChannel = [physicalChannel]
        else:
            self.physicalChannel = physicalChannel

        self.a = []

        self.CreateAIVoltageChan(
            ','.join(physicalChannel), "", DAQmx_Val_RSE,
            minv, maxv, DAQmx_Val_Volts, None
        )

        # scaling the buffer size
        #DAQmxCfgInputBuffer(self.taskHandle, self.bufferSize);

        '''int32 DAQmxCfgSampClkTiming (
            tasksHandle tasksHandle,
            const char source[],
            float64 rate,
            int32 activeEdge,
            int32 sampleMode,
            uInt64 sampsPerChanToAcquire
        );'''
        self.CfgSampClkTiming(
            'OnboardClock', rate, DAQmx_Val_Rising,
            DAQmx_Val_ContSamps, int(self.bufferSize*self.rate/4)
        )

        '''DAQmxRegisterEveryNSamplesEvent (
            TaskHandle task,
            int32 everyNsamplesEventType,
            uInt32 nSamples,
            uInt32 options,
            DAQmxEveryNSamplesEventCallbackPtr callbackFunction,
            void *callbackData
        );'''
        self.AutoRegisterEveryNSamplesEvent(
            DAQmx_Val_Acquired_Into_Buffer, self.samplesPerChannel, 0
        )
        self.AutoRegisterDoneEvent(0)

        self.digital_task = DigitalAcquisitionCallbackTask(
            digitalChannel, self.samplesPerChannel
        )

        self.time_plotter = linspace(0, 1, 1/self.samplesPerChannel)
        self.time_plotter = self.time_plotter[:self.samplesPerChannel]

    def EveryNCallback(self):
        read = int32()
        num_bytes = int32()

        self.data = zeros(self.bufferSize, dtype=numpy.float64)

        '''int32 DAQmxReadAnalogF64 (
            tasksHandle tasksHandle,
            int32 numSampsPerChan,
            float64 timeout,
            bool32 fillMode,
            float64 readArray[],
            uInt32 arraySizeInSamps,
            int32 *sampsPerChanRead,
            bool32 *reserved
        );'''

        # DAQmx_Val_GroupByScanNumber
        # DAQmx_Val_GroupByChannel
        self.ReadAnalogF64(
            self.samplesPerChannel, 10.0, DAQmx_Val_GroupByChannel,
            self.data, self.data.size, byref(read), None
        )

        _timing = calc_time(
            timedelta(seconds=1/self.samplesPerChannel),
            self.samplesPerChannel)

        # Create a ringbuffer or a temporary file to be used for other program
        # self.a.extend([self.data.tolist(), _timing])

        digital_data = self.digital_task.read()

        plt.clf()
        ax = plt.subplot(111)
        formatter = EngFormatter(unit='t', places=1)
        ax.xaxis.set_major_formatter(formatter)
        for i in xrange(self.numberOfChannel):
            plt.plot(
                self.data[self.samplesPerChannel*i:self.samplesPerChannel*(i+1)]
            )

            plt.plot(digital_data)

        plt.axis([0, self.samplesPerChannel-2, -2, 5])
        plt.grid()
        plt.draw()

        return 0  # The function should return an integer

    def DoneCallback(self, status):
        print("Status", status.value)
        return 0  # The function should return an integer

    def run(self):
        self.StartTask()

    def stop(self):
        self.StopTask()
        self.ClearTask()

        print('Acquisition stopped')


class DigitalAcquisitionCallbackTask(object):
    """

    """
    data = None
    a = None

    def __init__(self, physicalChannel=[], samples_per_channel=1.0):
        """

        """
        self.device_name = physicalChannel[0].split('/')[0]

        self.samplesPerChannel = int(samples_per_channel)

        self.bufferSize = len(physicalChannel) * self.samplesPerChannel
        self.numberOfChannel = physicalChannel.__len__()

        if isinstance(physicalChannel, str):
            self.physicalChannel = [physicalChannel]
        else:
            self.physicalChannel = physicalChannel

        self.a = []
        self.task = TaskHandle()
        DAQmxCreateTask("", byref(self.task))
        DAQmxCreateDIChan(
            self.task, ""
            ','.join(physicalChannel), "", DAQmx_Val_ChanForAllLines
        )

    def read(self):
        i_read = int32()
        num_bytes = int32()

        digital_data = zeros(self.samplesPerChannel, dtype=numpy.uint8)

        '''int32 DAQmxReadAnalogF64 (
            tasksHandle tasksHandle,
            int32 numSampsPerChan,
            float64 timeout,
            bool32 fillMode,
            float64 readArray[],
            uInt32 arraySizeInSamps,
            int32 *sampsPerChanRead,
            bool32 *reserved
        );'''

        DAQmxReadDigitalLines(
            self.task,
            self.samplesPerChannel, 10.0, DAQmx_Val_GroupByChannel,
            digital_data, digital_data.size,
            byref(i_read), byref(num_bytes), None
        )
        return digital_data

    def stop(self):
        DAQmxStopTask(self.task)
        DAQmxClearTask(self.task)
        print('Acquisition stopped')


class DaqPlotter(object):
    data = {}

    def __init__(self, devices, chunk):
        for d_name in devices:
            self.data[d_name] = [0]*chunk


def main():
    terminals = {}

    dev1_analog = ['Dev1/ai%s' % line for line in range(0, 10)]
    dev1_digital = ['Dev1/port0/line0']


    dev2 = ['Dev2/ai%s' % line for line in range(0, 4)]

    rate = 5000.

    plotter = DaqPlotter(['Dev1', 'Dev2'], int(rate))

    task_dev1 = AcquisitionCallbackTask(
        physicalChannel=dev1_analog,
        digitalChannel=dev1_digital,
        rate=rate, minv=-5.0, maxv=5.0
    )

    """
    task_dev2 = AcquisitionCallbackTask(
        physicalChannel=dev2, rate=rate, minv=-5.0, maxv=5.0,
        trigger='Dev1/di1'
    )
    """

    plt.ion()
    plt.show()

    task_dev1.run()
    #task_dev2.run()

    while True:
        try:
            raw_input('Acquiring samples continuously. Press CTRL + C to interrupt\n')
        except KeyboardInterrupt:
            break

    task_dev1.stop()
    #task_dev2.stop()
    plt.stop()

if __name__ == '__main__':
    main()