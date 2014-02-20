from __future__ import division, print_function
from datetime import timedelta
from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *
from numpy import zeros
from acquisition import calculate_time_sequence


class AnalogCallbackTask(Task):
    """

    """
    """

    """
    task = None
    physical_channels = None
    seconds_to_acquire = None
    rate = None
    samples_per_channel = None
    number_of_channels = None
    buffer_size = None
    buffer_daq_size = None
    minv = None
    maxv = None
    external_callback = None

    def __init__(
        self,
        physical_channels=[],
        rate=1000.,
        minv=(-5.0),
        maxv=5.0,
        seconds_to_acquire=3,
        samples_per_channel=1000,
        external_callback=()
    ):
        """

        """
        self.task = TaskHandle()
        self.physical_channels = physical_channels
        self.seconds_to_acquire = seconds_to_acquire
        self.rate = rate

        self.samples_per_channel = samples_per_channel
        self.number_of_channels = len(physical_channels)
        self.buffer_size = self.samples_per_channel * self.number_of_channels
        self.buffer_daq_size = self.buffer_size * self.rate/4  # w/ calibration
        self.external_callback = external_callback

        self.minv = minv
        self.maxv = maxv

        '''int32 DAQmxCreateAIVoltageChan (
            tasksHandle tasksHandle,
            const char physicalChannel[],
            const char nameToAssignToChannel[],
            int32 terminalsConfig,
            float64 minVal,
            float64 maxVal,
            int32 units,
            const char customScaleName[]
        );'''
        self.CreateAIVoltageChan(
            ','.join(physical_channels), "", DAQmx_Val_RSE,
            minv, maxv, DAQmx_Val_Volts, None
        )

        # scaling the buffer size
        DAQmxCfgInputBuffer(self.taskHandle, self.bufferSize)

        '''int32 DAQmxCfgSampClkTiming (
            tasksHandle tasksHandle,
            const char source[],
            float64 rate,
            int32 activeEdge,
            int32 sampleMode,
            uInt64 sampsPerChanToAcquire
        );'''
        self.CfgSampClkTiming(
            'OnboardClock', rate, DAQmx_Val_Rising,
            DAQmx_Val_ContSamps, self.samples_per_channel
        )

        '''DAQmxRegisterEveryNSamplesEvent (
            TaskHandle task,
            int32 everyNsamplesEventType,
            uInt32 nSamples,
            uInt32 options,
            DAQmxEveryNSamplesEventCallbackPtr callbackFunction,
            void *callbackData
        );'''
        self.AutoRegisterEveryNSamplesEvent(
            DAQmx_Val_Acquired_Into_Buffer, self.samples_per_channel, 0
        )
        self.AutoRegisterDoneEvent(0)

    def bind(self, callback):
        self.external_callback = callback

    def EveryNCallback(self):
        read = int32()
        data = zeros(self.bufferSize)

        '''int32 DAQmxReadAnalogF64 (
            tasksHandle tasksHandle,
            int32 numSampsPerChan,
            float64 timeout,
            bool32 fillMode,
            float64 readArray[],
            uInt32 arraySizeInSamps,
            int32 *sampsPerChanRead,
            bool32 *reserved
        );'''

        # DAQmx_Val_GroupByScanNumber
        # DAQmx_Val_GroupByChannel
        self.ReadAnalogF64(
            self.samplesPerChannel, 10.0, DAQmx_Val_GroupByChannel,
            self.data, self.data.size, byref(read), None
        )

        timing = calculate_time_sequence(
            timedelta(seconds=1/self.rate),
            self.samples_per_channel)

        self.external_callback(timing, data)

        return 0  # The function should return an integer

    def DoneCallback(self, status):
        print("Status", status.value)
        return 0  # The function should return an integer

    def run(self):
        self.StartTask()

    def stop(self):
        self.StopTask()
        self.ClearTask()

        print('Acquisition stopped')


class DigitalCallbackTask(Task):
    """

    """
    """

    """
    task = None
    physical_channels = None
    rate = None
    samples_per_channel = None
    number_of_channels = None
    buffer_size = None
    buffer_daq_size = None
    external_callback = ()

    def __init__(
        self, physical_channels=[], rate=1000., samples_per_channel=1000
    ):
        """

        """
        self.task = TaskHandle()
        self.physical_channels = physical_channels
        self.rate = rate

        self.samples_per_channel = samples_per_channel
        self.number_of_channels = len(physical_channels)
        self.buffer_size = self.samples_per_channel * self.number_of_channels
        self.buffer_daq_size = self.buffer_size * self.rate/4  # w/ calibration

        self.CreateDIChan(trigger, "", DAQmx_Val_ChanForAllLines)

        # scaling the buffer size
        DAQmxCfgInputBuffer(self.taskHandle, self.bufferSize)

        '''DAQmxRegisterEveryNSamplesEvent (
            TaskHandle task,
            int32 everyNsamplesEventType,
            uInt32 nSamples,
            uInt32 options,
            DAQmxEveryNSamplesEventCallbackPtr callbackFunction,
            void *callbackData
        );'''

        self.AutoRegisterEveryNSamplesEvent(
            DAQmx_Val_Acquired_Into_Buffer, self.samples_per_channel, 0
        )
        self.AutoRegisterDoneEvent(0)

    def bind(self, callback):
        self.external_callback = callback

    def EveryNCallback(self):
        read = int32()
        data = zeros(self.bufferSize)

        '''int32 DAQmxReadAnalogF64 (
            tasksHandle tasksHandle,
            int32 numSampsPerChan,
            float64 timeout,
            bool32 fillMode,
            float64 readArray[],
            uInt32 arraySizeInSamps,
            int32 *sampsPerChanRead,
            bool32 *reserved
        );'''

        # DAQmx_Val_GroupByScanNumber
        # DAQmx_Val_GroupByChannel
        self.ReadAnalogF64(
            self.samplesPerChannel, 10.0, DAQmx_Val_GroupByChannel,
            self.data, self.data.size, byref(read), None
        )

        timing = calc_time(
            timedelta(seconds=1/self.rate),
            self.samples_per_channel
        )

        self.external_callback(timing, data)

        return 0  # The function should return an integer

    def DoneCallback(self, status):
        print("Status", status.value)
        return 0  # The function should return an integer

    def run(self):
        self.StartTask()

    def stop(self):
        self.StopTask()
        self.ClearTask()

        print('Acquisition stopped')