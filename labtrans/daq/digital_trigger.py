# -*- coding: utf-8 -*-
from __future__ import print_function
import sys

from PyDAQmx import *
import numpy
import numpy as np
import time


def read_digital_port():
    # Declaration of variable passed by reference

    # data = numpy.zeros((15000,), dtype=numpy.float64)
    data = numpy.zeros((samplesPerChannel,), dtype=numpy.uint8)

    DAQmxReadDigitalLines(
        digitalTask,
        samplesPerChannel,
        10.0,
        DAQmx_Val_GroupByChannel,
        data,
        samplesPerChannel*10,
        byref(read),
        byref(bytesPerSamp),
        None
    )

    #print("Acquired %d points\n" % read.value)

    #print data

    if any(map(lambda v: v > 0.0, data)):
        print('\rON ', end='')
    else:
        print('\rOFF', end='')
    sys.stdout.flush()


digitalTask = TaskHandle()

_channel = "Dev2/port0/line0"

read = int32()
bytesPerSamp = int32()
samplesPerChannel = 1

# DAQmx Configure Code
DAQmxCreateTask("", byref(digitalTask))

DAQmxCreateDIChan(digitalTask, _channel, "", DAQmx_Val_ChanPerLine)
DAQmxStartTask(digitalTask)

while True:
    try:
        read_digital_port()
    except KeyboardInterrupt:
        DAQmxStopTask(digitalTask)
        DAQmxClearTask(digitalTask)
        print('\nTask stopped')
        print('Quit')
        break
