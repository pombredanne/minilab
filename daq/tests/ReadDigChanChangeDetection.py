# -*- coding: utf-8 -*-
"""
/*********************************************************************
*
* ANSI C Example program:
*    ReadDigChan-ChangeDetection.c
*
* Example Category:
*    DI
*
* Description:
*    This example demonstrates how to read values from one or more
*    digital input channels using change detection.
*
* Instructions for Running:
*    1. Select the digital lines on the DAQ device to be read.
*    2. Select the rising and falling edge lines on which to perform
*       change detection.
*    3. Select the number of samples per read.
*
* Steps:
*    1. Create a task.
*    2. Create a Digital Input channel. Use one channel for all
*       lines. You can alternatively use one channel for each line, 
*       but then use a different version of the DAQmx Read function.
*    3. Setup the Change Detection timing for the acquisition. The
*       timing is set to read continuously. The Rising Edge Lines and
*       Falling Edge Lines specify on which digital lines a change
*       causes a sample to be read.
*    4. Call the Start function to start the task.
*    5. Read the digital data continuously until the user hits the
*       stop button or an error occurs. This read function reads
*       Samples Per Read samples of digital data every time. Also set
*       a timeout so an error is returned if the samples are not
*       returned within the specified time limit. Because this
*       example uses change detection,  10 seconds was chosen as an
*       arbitrarily large number to allow for changes to occur.
*    6. Call the Clear Task function to clear the task.
*    7. Display an error if any.
*
* I/O Connections Overview:
*    Make sure your signal input terminals match the Lines I/O
*    Control. In this case wire your digital signals to the first
*    eight digital lines on your DAQ Device.
*
*    Note: For NI 6534 devices either 32 bytes of data needs to be
*          transferred first for the DMA transfer to take place,  or
*          interrupts must be used instead of DMA.
*
*********************************************************************/
"""
from PyDAQmx import *
import numpy as np

def DAQmxErrChk(error):
    if error < 0:
        raise Exception('DAQ ERROR')


def main():
    taskHandle = TaskHandle()
    data = np.zeros((32, ),  dtype=np.uint8)
    numRead = int32()
    bytesPerSamp = int32()

    num_channels = 1
    samples_per_channel = 4

    # /*********************************************/
    # // DAQmx Configure Code
    # /*********************************************/
    DAQmxErrChk(DAQmxCreateTask("", byref(taskHandle)))
    DAQmxErrChk(
        DAQmxCreateDIChan(
            taskHandle, "Dev4/port0/line0", "", DAQmx_Val_ChanPerLine)
    )
    DAQmxErrChk(
        DAQmxCfgChangeDetectionTiming(
            taskHandle, "Dev1/port0/line0",
            "Dev1/port0/line0", DAQmx_Val_ContSamps,
            samples_per_channel * num_channels)
    )

    # /*********************************************/
    # // DAQmx Start Code
    # /*********************************************/
    DAQmxErrChk(DAQmxStartTask(taskHandle))

    print("Continuously reading. Press Ctrl+C to interrupt\n")

    while True:
        # /*********************************************/
        # // DAQmx Read Code
        # /*********************************************/
        try:
            DAQmxErrChk(
                DAQmxReadDigitalLines(
                    taskHandle, samples_per_channel, 10.0,
                    DAQmx_Val_GroupByScanNumber,
                    data, samples_per_channel*num_channels,
                    byref(numRead), byref(bytesPerSamp), None)
            )
            print(data)
        except:
            print('Timeout.')

if __name__ == '__main__':
    main()