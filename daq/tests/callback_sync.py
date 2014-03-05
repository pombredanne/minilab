from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *

import numpy as np
import time

AItaskHandle = object()
DItaskHandle = object()

class InternalList(list):
    pass

def GetTerminalNameWithDevPrefix(
    taskHandle, terminalName, triggerName
):
    error=0
    device = create_string_buffer(256)
    productCategory = int32()
    numDevices = uInt32()
    i = 1

    DAQmxGetTaskNumDevices(taskHandle, numDevices);

    while i<=numDevices:
        DAQmxGetNthTaskDevice(taskHandle,i,device,256)
        i += 1
        DAQmxGetDevProductCategory(device, productCategory)

        if(
            productCategory!=DAQmx_Val_CSeriesModule and
            productCategory!=DAQmx_Val_SCXIModule
        ):
            triggerName.value += '/'
            triggerName.value += device.value + terminalName
            break


def EveryNCallback_py(
    taskHandle,
    everyNsamplesEventType,
    nSamples,
    callbackData_ptr
):
    callbackData = get_callbackdata_from_id(callbackData_ptr)
    totalAI=0
    totalDI=0
    readAI = int32()
    readDI = int32()

    AIdata = numpy.zeros((1000,), dtype=numpy.float64)
    DIdata = numpy.zeros((1000,), dtype=numpy.uint32);

    #/*********************************************/
    #// DAQmx Read Code
    #/*********************************************/
    DAQmxReadAnalogF64(
        AItaskHandle,1000,10.0,
        DAQmx_Val_GroupByChannel,
        AIdata,1000, byref(readAI),None
    )

    DAQmxReadDigitalU32(
        DItaskHandle,1000,10.0,
        DAQmx_Val_GroupByChannel,DIdata,1000,byref(readDI),None
    )

    print(
        "%d\t%d\r" %
        (readAI.value,readDI.value)
    )
    return 0


def DoneCallback_py(
    taskHandle, status, callbackData
):
    pass


# main
d_task = TaskHandle()
a_task = TaskHandle()

AItaskHandle = a_task
DItaskHandle = d_task

trigName = create_string_buffer(256)

channels = "Dev4/ai0, Dev4/ai1"

# tasks
DAQmxCreateTask("",byref(a_task))
DAQmxCreateAIVoltageChan(
    a_task,channels,"",
    DAQmx_Val_Cfg_Default,-10.0,10.0,DAQmx_Val_Volts,None
)
DAQmxCfgSampClkTiming(
    a_task,"",5000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,100000
)

GetTerminalNameWithDevPrefix(a_task, "ai/SampleClock", trigName)
"""
int32 CVICALLBACK EveryNCallback(
    TaskHandle taskHandle, int32 everyNsamplesEventType,
    uInt32 nSamples, void *callbackData
)
"""

internal_list = InternalList()
id_every_n = create_callbackdata_id(internal_list)

EveryNCallback = DAQmxEveryNSamplesEventCallbackPtr(EveryNCallback_py)

DAQmxRegisterEveryNSamplesEvent(
    AItaskHandle,DAQmx_Val_Acquired_Into_Buffer,
    10000,0,EveryNCallback,id_every_n
)
#DAQmxRegisterDoneEvent(AItaskHandle,0,DoneCallback,None)

# digital

DAQmxCreateTask("", byref(d_task)) # digital
DAQmxCreateDIChan(
    d_task,
    ','.join(['Dev4/port0/line31']),
    '',
    DAQmx_Val_ChanPerLine
)
DAQmxCfgSampClkTiming(
    DItaskHandle,'',5000.0,DAQmx_Val_Rising,DAQmx_Val_ContSamps,10000
)

DAQmxStartTask(d_task)
DAQmxStartTask(a_task)

samples_per_channel = 1000
num_channels = channels.split(',').__len__()

samps_per_chan_read_i = int32()
bytes_per_samp_i = int32()


while True:
    raw_input('Press <ENTER> to read digital signal.')

    data = np.zeros((samples_per_channel*num_channels,), dtype=np.uint8)

    t = time.time()

    DAQmxReadDigitalLines(
        d_task,
        samples_per_channel,
        10.0,
        DAQmx_Val_GroupByChannel,
        data,
        samples_per_channel,
        byref(samps_per_chan_read_i),
        byref(bytes_per_samp_i),
        None
    )

    print('Exec Time: %s' % (time.time() - t))

DAQmxStopTask(d_task)
DAQmxClearTask(d_task)