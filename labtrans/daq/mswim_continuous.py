# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""
from __future__ import print_function, division
from PyDAQmx import *
from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *

import numpy
import time


class AcquisitionFiniteTask():
    """Class to create an multi-channel analog input

    Utilisation: AI = MultiChannelInput(physicalChannel)
        physicalChannel: a string or a list of string
    optional parameter: limit: tuple or list of tuple, the AI limit values
                        reset: booleen
    Methodes:
        read(name), return the value of the input name
        readAll(), return a dictionnary name:value
    """

    taskHandles = None

    def __init__(self, physicalChannel=[], rate=1.0, minv=-5.0, maxv=5.0):
        """

        """
        self.physicalChannel = physicalChannel
        self.numberOfChannel = physicalChannel.__len__()
        self.samplesPerChannel = 1
        self.rate = rate

        self.limit = dict(
            [(name, (minv, maxv)) for name in self.physicalChannel]
        )

        # Immediately aborts all tasks associated with a device and returns the
        # device to an initialized state. Aborting a task stops and
        # releases any resources the task reserved.
        # DAQmxResetDevice(physicalChannel[0].split('/')[0])

        # Configures acquisitions
        self.configure()

    def configure(self):
        # Create one task handle per Channel
        taskHandles = dict(
            [(name, TaskHandle(0)) for name in self.physicalChannel]
        )

        for name in self.physicalChannel:
            DAQmxCreateTask('', byref(taskHandles[name]))
            DAQmxCreateAIVoltageChan(
                taskHandles[name], name, "", DAQmx_Val_RSE,
                self.limit[name][0], self.limit[name][1],
                DAQmx_Val_Volts, None
            )
            DAQmxCfgSampClkTiming(
                taskHandles[name], '', self.rate, DAQmx_Val_Rising,
                DAQmx_Val_ContSamps, self.samplesPerChannel
            )
        self.taskHandles = taskHandles

    def readAll(self):
        return dict([(name, self.read(name)) for name in self.physicalChannel])

    def read(self, name=None):
        if not name:
            name = self.physicalChannel[0]

        taskHandle = self.taskHandles[name]

        DAQmxStartTask(taskHandle)
        data = numpy.zeros((1,), dtype=numpy.float64)

#        data = AI_data_type()
        read = int32()
        DAQmxReadAnalogF64(
            taskHandle, 1, 10.0,
            DAQmx_Val_GroupByChannel, data, 1, byref(read), None
        )
        DAQmxStopTask(taskHandle)

        return data[0], time.time()


if __name__ == '__main__':
    dev1 = ['Dev1/ai%s' % line for line in range(0, 16)]
    dev2 = ['Dev2/ai%s' % line for line in range(0, 16)]

    task_dev = AcquisitionFiniteTask(
        physicalChannel=dev1 + dev2, rate=5000., minv=-5.0, maxv=5.0
    )

    print('processando ... PRESSIONE CTRL+C PARA INTERROMPER O PROCESSO')

    while True:
        print(task_dev.readAll())
        time.sleep(0.0002)