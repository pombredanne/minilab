# -*- coding: utf8 -*-
"""
Writes multiple floating-point samples to a task that contains
one or more analog output channels.

Note: If you configured timing for your task, your write is considered a
buffered write. Buffered writes require a minimum buffer size of 2 samples.
If you do not configure the buffer size using DAQmxCfgOutputBuffer,
NI-DAQmx automatically configures the buffer when you configure sample timing.
If you attempt to write one sample for a buffered write without configuring
the buffer, you will receive an error.

"""
from __future__ import print_function
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from PyDAQmx import *

import numpy as np

# configuração
rate = 100
sampling = 1000
channel = 'Dev1/ao0'

tasks = TaskHandle()
buffer = int32()

# tarefa

# DAQmx Configure Code
DAQmxCreateTask('', byref(tasks))

DAQmxCreateAOVoltageChan(
    tasks,
    channel,
    '',
    -5.0,
    5.0,
    DAQmx_Val_Volts,
    None
)

DAQmxCfgSampClkTiming(
    tasks,
    '',
    rate,
    DAQmx_Val_Rising,
    DAQmx_Val_FiniteSamps,
    sampling
)

#samp = np.sin(np.linspace(0, 1, sampling))
samp = np.array([0.]*250 + [4.]*500 + [0.]*250)
#samp = np.array([0.]*1000)+1
#samp = np.array(range(sampling))/float(sampling)

#plt.plot(samp)
#plt.show()
#exit()
#DAQmxStartTask(tasks)
for _ in range(10):
    DAQmxWriteAnalogF64(
        tasks,
        sampling,
        True,
        10.0,
        DAQmx_Val_GroupByChannel,
        samp,
        byref(buffer),
        None
    )

    # Declaration of variable passed by reference
    # DAQmxStartTask(tasks[channel])
    # DAQmxStopTask(tasks[channel])

    DAQmxWaitUntilTaskDone(tasks, 10.0)
    DAQmxStopTask(tasks)

DAQmxClearTask(tasks)
