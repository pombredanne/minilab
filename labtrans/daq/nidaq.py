from __future__ import print_function
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from collections import defaultdict
from time import sleep
from PyDAQmx import *

import numpy as np
import time
import sys


class DAQTask():
    tasks = {}

    def __init__(self, physical_channels, rate=1000, sampling=100):
        # DAQmxResetDevice(physical_channels[0].split('/')[0])
        for channel in physical_channels:
            self.tasks[channel] = TaskHandle()

            # DAQmx Configure Code
            DAQmxCreateTask(
                '',
                byref(self.tasks[channel])
            )

            DAQmxCreateAOVoltageChan(
                self.tasks[channel],
                channel,
                '',
                -5.0,
                5.0,
                DAQmx_Val_Volts,
                None
            )

            #DAQmxCfgOutputBuffer(tasks[channel], 1000);

            DAQmxCfgSampClkTiming(
                self.tasks[channel],
                '',
                rate,
                DAQmx_Val_Rising,
                DAQmx_Val_ContSamps,
                sampling
            )

            #DAQmxWriteAnalogScalarF64(tasks[channel], True, 10.0, 0.0, None)
            '''
            DAQmxWriteAnalogF64 (
                TaskHandle taskHandle,
                int32 numSampsPerChan,
                bool32 autoStart,
                float64 timeout,
                bool32 dataLayout,
                float64 writeArray[],
                int32 *sampsPerChanWritten,
                bool32 *reserved
            );
            '''

            write = int32()

            DAQmxWriteAnalogF64(
                self.tasks[channel],
                sampling,
                True,
                10.0,
                DAQmx_Val_GroupByChannel,
                np.zeros(sampling),
                byref(write),
                None
            )

            # Declaration of variable passed by reference
            # DAQmxStartTask(tasks[channel])

    def write(self, plotting=False):
        if plotting:
            plt.ion()
            plt.show()

        write = int32()

        window_width = 15000
        update_rate = 100
        window = [[0] * window_width] * 4

        list_time = np.arange(0, window_width, 1)