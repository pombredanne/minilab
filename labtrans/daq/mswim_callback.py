# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:04:42 2013

@author: ivan
"""
from __future__ import division, print_function
from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from numpy import zeros
from datetime import datetime, timedelta
from matplotlib import pyplot as plt

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
    data = None
    a = None

    def __init__(self, physicalChannel=[], rate=1.0, minv=-5.0, maxv=5.0):
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

        # DAQmxResetDevice(dev[0].split('/')[0])

        '''int32 DAQmxCreateAIVoltageChan (
            tasksHandle tasksHandle,
            const char physicalChannel[],
            const char nameToAssignToChannel[],
            int32 terminalsConfig,
            float64 minVal,
            float64 maxVal,
            int32 units,
            const char customScaleName[]
        );'''
        self.CreateAIVoltageChan(
            ','.join(physicalChannel), "", DAQmx_Val_RSE,
            minv, maxv, DAQmx_Val_Volts, None
        )

        # scaling the buffer size
        DAQmxCfgInputBuffer(self.taskHandle, self.bufferSize);

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
            DAQmx_Val_ContSamps, self.samplesPerChannel
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

    def EveryNCallback(self):
        read = int32()
        self.data = zeros(self.bufferSize)

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

        plt.clf()
        #ax = plt.subplot(111)
        #ax.set_xscale('log')
        #formatter = EngFormatter(unit='t', places=1)
        #ax.xaxis.set_major_formatter(formatter)
        plt.plot(self.data[:self.samplesPerChannel])
        plt.plot(self.data[self.samplesPerChannel:self.samplesPerChannel*2])
        plt.plot(self.data[self.samplesPerChannel*2:self.samplesPerChannel*3])
        plt.plot(self.data[self.samplesPerChannel*4:])

        plt.axis([0, self.samplesPerChannel-2, -2, 5])
        plt.grid()
        plt.draw()

        return 0  # The function should return an integer

    def DoneCallback(self, status):
        print("Status", status.value)
        return 0  # The function should return an integer

    def run(self):
        self.StartTask()

        try:
            plt.ion()
            plt.show()
        except:
            pass

    def stop(self):
        self.StopTask()
        self.ClearTask()

        print('Acquisition stopped')


def test():
    terminals = {}

    dev1 = ['Dev1/ai%s' % line for line in range(0, 4)]
    dev2 = ['Dev2/ai%s' % line for line in range(0, 4)]

    task_dev1 = AcquisitionCallbackTask(
        physicalChannel=dev2, rate=5000., minv=-5.0, maxv=5.0
    )
    '''
    task_dev2 = AcquisitionCallbackTask(
        physicalChannel=dev2, rate=5000., minv=-5.0, maxv=5.0
    )
    '''

    task_dev1.run()
    #task_dev2.run()

    while True:
        try:
            raw_input('Acquiring samples continuously. Press CTRL + C to interrupt\n')
        except KeyboardInterrupt:
            break

    task_dev1.stop()

    #task_dev2.stop()

if __name__ == '__main__':
    test()