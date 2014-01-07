# -*- coding: utf-8 -*-
import sys
# append location of mswim module
sys.path.append('/'.join(sys.path[0].split('/')[:-2]) + '/mswim/')
#sys.path.append('c:/dev/labtrans/mswim/')

from devices.cam2 import FXCamd102
    
from PyDAQmx import *
import numpy
import numpy as np
import time as ttime

_channel = "dev1/port0/line5"

while True:
    taskHandle = TaskHandle()
    read = int32()
    
    # DAQmx Configure Code
    DAQmxCreateTask("",byref(taskHandle))
        
    ##DAQmxCreateAIVoltageChan(taskHandle,_channel,"",DAQmx_Val_Cfg_Default,-5.0,5.0,DAQmx_Val_Volts,None)
    #DAQmxCreateDIChan(TaskHandle taskHandle, const char lines[], const char nameToAssignToLines[], int32 lineGrouping);
    DAQmxCreateDIChan(taskHandle, _channel, "", DAQmx_Val_ChanPerLine)
    
    #DAQmxCfgSampClkTiming(TaskHandle taskHandle, const char source[], float64 rate, int32 activeEdge, int32 sampleMode, uInt64 sampsPerChan);
    ##DAQmxCfgSampClkTiming(taskHandle,"",15000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,15000)
    #DAQmxCfgHandshakingTiming(TaskHandle taskHandle, int32 sampleMode, uInt64 sampsPerChan);
    #XDAQmxCfgHandshakingTiming(taskHandle, DAQmx_Val_ChangeDetection,15000)
    #DAQmxCfgSampClkTiming(taskHandle,_channel,15000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,15000)
    DAQmxCfgChangeDetectionTiming(taskHandle,_channel,"", DAQmx_Val_ContSamps,15000)
    
    # Declaration of variable passed by reference
    
    #data = numpy.zeros((15000,), dtype=numpy.float64)
    data = numpy.zeros((15000,), dtype=numpy.int8)
    DAQmxStartTask(taskHandle)
    #DAQmx Start Code
    try: 
        #int32 DAQmxReadAnalogF64(
        #  TaskHandle taskHandle, int32 numSampsPerChan, float64 timeout, 
        #  bool32 fillMode, float64 readArray[], uInt32 arraySizeInSamps, 
        #  int32 *sampsPerChanRead, bool32 *reserved);
        ##DAQmxReadAnalogF64(taskHandle,15000,10.0,DAQmx_Val_GroupByChannel,data,15000,byref(read),None)
        #DAQmxGetReadDigitalLinesBytesPerChan
        #>DAQmxReadDigitalLines(
        #   TaskHandle taskHandle, int32 numSampsPerChan, float64 timeout, 
        #   bool32 fillMode, uInt8 readArray[], uInt32 arraySizeInBytes, 
        #   int32 *sampsPerChanRead, int32 *numBytesPerSamp, bool32 *reserved)
        pass
    except:
        pass
    DAQmxReadDigitalLines(taskHandle,15000,10.0,DAQmx_Val_GroupByChannel,data,15000,byref(read),15000, None)
    #print("Acquired %d points\n" % read.value)
    
    
    print data
    
    if any(map(lambda v: v > 0.0, data)):
        cam = FXCamd102('192.168.1.97')
        imageid = cam.send_trigger(True)
        im = cam.image(imageid)
        open('%s.jpg' % imageid, 'wb').write(im)
        lplate = cam.license_plate(imageid)
        
        print('License Plate: %s' % lplate)
        print(cam.time(imageid))
        print(data)
        exit()
    
    ttime.sleep(0.1)
    DAQmxStopTask(taskHandle)
    DAQmxClearTask(taskHandle)