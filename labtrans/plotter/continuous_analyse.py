# -*- coding: utf-8 -*-
from PyDAQmx import *
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy
import numpy as np
import time as ttime

plt.ion()
plt.show()


time = numpy.arange(0, 3, 0.0002)

taskHandle = TaskHandle()
read = int32()

# DAQmx Configure Code
DAQmxCreateTask("",byref(taskHandle))
DAQmxCreateAIVoltageChan(taskHandle,"dev1/ai0","",DAQmx_Val_Cfg_Default,-5.0,5.0,DAQmx_Val_Volts,None)
DAQmxCfgSampClkTiming(taskHandle,"",5000.0,DAQmx_Val_Rising, DAQmx_Val_ContSamps,15000)

# Declaration of variable passed by reference
DAQmxStartTask(taskHandle)

while True:
    data = numpy.zeros((15000,), dtype=numpy.float64)

    #DAQmx Start Code
    try: 
        DAQmxReadAnalogF64(taskHandle,15000,10.0,DAQmx_Val_GroupByChannel,data,15000,byref(read),None)
    except:
        pass
    
    #print("Acquired %d points\n" % read.value)
    
    plt.clf()
    ax = plt.subplot(111)
    #ax.set_xscale('log')
    formatter = EngFormatter(unit='Hz', places=1)
    ax.xaxis.set_major_formatter(formatter)
    
    #xs = np.logspace(1, 9, 100)
    #ys = (0.8 + 0.4 * np.random.uniform(size=100)) * np.log10(xs)**2
    
    ax.plot(time, data)
    
    plt.draw()
    ttime.sleep(0.0002)

DAQmxStopTask(taskHandle)
#DAQmxClearTask(taskHandle)