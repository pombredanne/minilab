# -*- coding: utf-8 -*-
from __future__ import print_function
from PyDAQmx import *
from mswim_finite_time import AcquisitionFiniteTask

import traceback
import sys
import numpy
import numpy as np
import time


class WimTask():
    """

    """

    digital_task = None
    analogic_task = None
    channel = None
    read = None
    bytes_per_samp = None
    samples_per_channel = None

    def __init__(self):
        """

        @return:
        """
        self.configure()

    def configure(self):
        """

        @return:
        """

        self.digital_task = TaskHandle()


        self.channel = "Dev2/port0/line0"

        self.read = int32()
        self.bytes_per_samp = int32()
        self.samples_per_channel = 1

        self.dev1 = ['Dev1/ai%s' % line for line in range(0, 4)]
        self.dev2 = ['Dev2/ai%s' % line for line in range(0, 4)]


    def read_digital_port(self):
        # Declaration of variable passed by reference

        # data = numpy.zeros((15000,), dtype=numpy.float64)
        data = numpy.zeros((self.samples_per_channel,), dtype=numpy.uint8)

        # DAQmx Configure Code
        DAQmxCreateTask("", byref(self.digital_task))
        DAQmxCreateDIChan(
            self.digital_task, self.channel, "", DAQmx_Val_ChanPerLine
        )

        DAQmxStartTask(self.digital_task)

        DAQmxReadDigitalLines(
            self.digital_task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.samples_per_channel*2,
            byref(self.read),
            byref(self.bytes_per_samp),
            None
        )

        DAQmxStopTask(self.digital_task)
        DAQmxClearTask(self.digital_task)

        #print("Acquired %d points\n" % read.value)

        #print data

        if any(map(lambda v: v > 0.0, data)):
            print('\rON ', end='')
            sys.stdout.flush()

            task_dev = AcquisitionFiniteTask(
                physical_channel=self.dev2, rate=5000., minv=-5.0, maxv=5.0
            )

            data = task_dev.read()
            task_dev.plot(data)

            del task_dev

        else:
            print('\rOFF', end='')
            sys.stdout.flush()

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

task = WimTask()

while True:
    try:
        task.read_digital_port()
    except KeyboardInterrupt:
        task.clear()
        break
    except Exception as e:
        print('Fatal error: %s' % traceback.format_exc())
        break
