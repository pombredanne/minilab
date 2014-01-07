# -*- coding: utf-8 -*-
import sys
# append location of mswim module
#sys.path.append('/home/ivan/dev/pydev/labtrans/mswim/')
sys.path.append('c:/dev/labtrans/mswim/')

from devices.cam2 import FXCamd102
    
from PyDAQmx import *
import numpy
import numpy as np
import time as ttime

while True:
    taskHandle = TaskHandle()
    read = int32()
    
    # DAQmx Configure Code
    DAQmxCreateTask("",byref(taskHandle))
    DAQmxCreateAIVoltageChan(taskHandle,"dev1/ai0","",DAQmx_Val_Cfg_Default,-5.0,5.0,DAQmx_Val_Volts,None)
    DAQmxCfgSampClkTiming(taskHandle,"",15000.0,DAQmx_Val_Rising,DAQmx_Val_FiniteSamps,15000)
    # Declaration of variable passed by reference
    
    data = numpy.zeros((15000,), dtype=numpy.float64)
    DAQmxStartTask(taskHandle)
    #DAQmx Start Code
    try: 
        DAQmxReadAnalogF64(taskHandle,15000,10.0,DAQmx_Val_GroupByChannel,data,15000,byref(read),None)
    except:
        pass
    
    #print("Acquired %d points\n" % read.value)
    DAQmxStopTask(taskHandle)
    DAQmxClearTask(taskHandle)
    
    if any(map(lambda v: v > 0.01, data)):
        cam = FXCamd102('192.168.1.97')
        imageid = cam.send_trigger(True)
        im = cam.image(imageid)
        open('%s.jpg' % imageid, 'wb').write(im)
        lplate = cam.license_plate(imageid)
        
        print('License Plate: %s' % lplate)
        print(cam.time(imageid))
        exit()
    
    ttime.sleep(0.1)