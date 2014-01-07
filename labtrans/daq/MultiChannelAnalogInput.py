# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""

import numpy
import time

from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *

terminals = {}

terminals['Dev1'] = ['Dev1/ai%s' % line for line in range(0, 2)]
terminals['Dev2'] = ['Dev2/ai%s' % line for line in range(0, 16)]

class MultiChannelAnalogInput():
    """Class to create an multi-channel analog input

    Utilisation: AI = MultiChannelInput(physicalChannel)
        physicalChannel: a string or a list of string
    optional parameter: limit: tuple or list of tuple, the AI limit values
                        reset: booleen
    Methodes:
        read(name), return the value of the input name
        readAll(), return a dictionnary name:value
    """
    def __init__(self,physicalChannel, limit = None, reset = False):
        if type(physicalChannel) == type(""):
            self.physicalChannel = [physicalChannel]
        else:
            self.physicalChannel  =physicalChannel
        self.numberOfChannel = physicalChannel.__len__()
        if limit is None:
            self.limit = dict([(name, (-5.0,5.0)) for name in self.physicalChannel])
        elif type(limit) == tuple:
            self.limit = dict([(name, limit) for name in self.physicalChannel])
        else:
            self.limit = dict([(name, limit[i]) for  i,name in enumerate(self.physicalChannel)])
        if reset:
            DAQmxResetDevice(physicalChannel[0].split('/')[0] )
    def configure(self):
        # Create one task handle per Channel
        taskHandles = dict([(name,TaskHandle(0)) for name in self.physicalChannel])
        for name in self.physicalChannel:
            DAQmxCreateTask("",byref(taskHandles[name]))
            DAQmxCreateAIVoltageChan(taskHandles[name],name,"",DAQmx_Val_RSE,
                                     self.limit[name][0],self.limit[name][1],
                                     DAQmx_Val_Volts,None)
        self.taskHandles = taskHandles
    def readAll(self):
        return dict([(name, self.read(name)) for name in self.physicalChannel])
    def read(self,name = None):
        if name is None:
            name = self.physicalChannel[0]
        taskHandle = self.taskHandles[name]
        DAQmxStartTask(taskHandle)
        data = numpy.zeros((1,), dtype=numpy.float64)

#        data = AI_data_type()
        read = int32()
        DAQmxReadAnalogF64(taskHandle,1,10.0,DAQmx_Val_GroupByChannel,data,1,byref(read),None)
        DAQmxStopTask(taskHandle)

        return data[0], time.time()


if __name__ == '__main__':
    multipleAI = MultiChannelAnalogInput(terminals['Dev1'])
    multipleAI.configure()
    while True:
        print multipleAI.readAll()
        time.sleep(0.0002)