# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""
from __future__ import print_function, division
from PyDAQmx import *
from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
from matplotlib import pyplot as plt
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np
import random


from mswim.apps.acquisition.models import AcquisitionModel


def calc_time(delta_t, N):
    timestamp = [datetime.now()]

    def next_time(tstamp):
        _ts = tstamp[0]
        tstamp[0] += delta_t
        return _ts

    return [next_time(timestamp) for _ in range(N)]


class AcquisitionFiniteTask():
    """

    """
    task = None
    physical_channel = None
    seconds_to_acquire = None
    rate = None
    samples_per_channel = None
    number_of_channels = None
    buffer_size = None
    minv = None
    maxv = None

    def __init__(
        self,
        physical_channel=[],
        rate=1.0,
        minv=(-5.0),
        maxv=5.0,
        seconds_to_acquire=3
    ):
        """

        """
        self.task = TaskHandle()
        self.physical_channel = physical_channel
        self.seconds_to_acquire = seconds_to_acquire
        self.rate = rate
        self.samples_per_channel = int(self.rate * self.seconds_to_acquire)
        self.number_of_channels = len(physical_channel)
        self.buffer_size = self.samples_per_channel * self.number_of_channels

        self.minv = minv
        self.maxv = maxv

        DAQmxCreateTask('AcquisitionFiniteTask', byref(self.task))

        DAQmxCreateAIVoltageChan(
            self.task,
            ','.join(self.physical_channel),
            '',
            DAQmx_Val_RSE,
            self.minv,
            self.maxv,
            DAQmx_Val_Volts,
            None
        )

        # note: Finite time raise -200284 error
        DAQmxCfgSampClkTiming(
            self.task,
            '',
            self.rate,
            DAQmx_Val_Rising,
            DAQmx_Val_ContSamps,
            self.samples_per_channel
        )


    def read(self):
        """
        @return: data acquisitions, time of each acquisition
        """
        data = self._read()

        return dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channel)
        ]), calc_time(timedelta(1 / self.rate), self.samples_per_channel)


    def _read(self):
        DAQmxStartTask(self.task)
        data = np.zeros(
            self.buffer_size,
            dtype=np.float64
        )

        # data = AI_data_type()
        read = int32()
        DAQmxReadAnalogF64(
            self.task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.buffer_size,
            byref(read),
            None
        )

        # DAQmxWaitUntilTaskDone(self.task, 10.0)  # only for FiniteSamps mode
        DAQmxStopTask(self.task)
        # DAQmxClearTask(self.task)

        return data


class AcquisitionCallbackTask(Task):
    """

    """
    data = None
    buffer = None
    callback = None

    def __init__(
        self,
        physical_channel=[],
        seconds_to_acquire=0.0,
        rate=1.0,
        minv=(-5.0),
        maxv=5.0,
        callback=None
    ):
        """

        """
        Task.__init__(self)

        self.device_name = physical_channel[0].split('/')[0]

        self.rate = rate
        self.minv = minv
        self.maxv = maxv
        self.samplesPerChannel = int(rate * seconds_to_acquire)

        self.bufferSize = len(physical_channel) * self.samplesPerChannel
        self.numberOfChannel = physical_channel.__len__()

        if type(physical_channel) == type(""):
            self.physical_channel = [physical_channel]
        else:
            self.physical_channel = physical_channel

        self.buffer = []

        self.CreateAIVoltageChan(
            ','.join(physical_channel), "", DAQmx_Val_RSE,
            minv, maxv, DAQmx_Val_Volts, None
        )

        # scaling the buffer size
        DAQmxCfgInputBuffer(self.taskHandle, self.bufferSize);

        self.CfgSampClkTiming(
            'OnboardClock', rate, DAQmx_Val_Rising,
            DAQmx_Val_ContSamps, self.samplesPerChannel
        )

        self.AutoRegisterEveryNSamplesEvent(
            DAQmx_Val_Acquired_Into_Buffer, self.samplesPerChannel, 0
        )

        self.callback = callback
        self.AutoRegisterDoneEvent(0)

    def EveryNCallback(self):
        read = int32()
        self.data = np.zeros(self.bufferSize)

        # DAQmx_Val_GroupByScanNumber
        # DAQmx_Val_GroupByChannel
        self.ReadAnalogF64(
            self.samplesPerChannel, 10.0, DAQmx_Val_GroupByChannel,
            self.data, self.data.size, byref(read), None
        )

        # buffer
        # self.buffer += self.data

        _timing = calc_time(
            timedelta(seconds=1 / self.samplesPerChannel),
            self.samplesPerChannel)

        if self.callback:
            self.callback(self.data, self.samplesPerChannel)

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


class AcquisitionDigitalTask(object):
    """

    """
    digital_task = None
    channels = None
    read_int32 = None
    bytes_per_samp_int32 = None
    samples_per_channel = None

    def __init__(
        self,
        channels,
        samples_per_channel
    ):
        self.digital_task = TaskHandle()
        self.channels = channels
        self.samples_per_channel = samples_per_channel
        self.read_int32 = int32()
        self.bytes_per_samp_int32 = int32()

    def read(self):
        """

        """
        data = numpy.zeros((self.samples_per_channel,), dtype=numpy.uint8)

        DAQmxCreateTask("", byref(self.digital_task))
        DAQmxCreateDIChan(
            self.digital_task,
            ','.join(self.channels),
            '',
            DAQmx_Val_ChanPerLine
        )

        DAQmxStartTask(self.digital_task)

        DAQmxReadDigitalLines(
            self.digital_task,
            self.samples_per_channel,
            10.0,
            DAQmx_Val_GroupByChannel,
            data,
            self.samples_per_channel * 2,
            byref(self.read_int32),
            byref(self.bytes_per_samp_int32),
            None
        )

        DAQmxStopTask(self.digital_task)
        DAQmxClearTask(self.digital_task)

        return data

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


class AcquisitionTask():
    """

    """
    ACQ_TYPE = {
        'test': 2,
        'calibration': 3,
        'statistic': 1
    }

    trigger_task = None
    channel = None
    is_simulated = None
    task_device = None
    acquisition_type = None

    def __init__(self,
        trigger_channel='',
        channels=[],
        minv=0,
        maxv=0,
        rate=1,
        seconds_to_acquire=1,
        plotting=False,
        sensor_type=0,
        temperature_sensor=False,
        temperature_path=None,
        is_simulated=False,
        callback=None,
        acquisition_type=None
    ):
        """

        @return:

        """
        self.channels = channels

        self.sensor_type = sensor_type
        self.plotting = plotting
        self.temperature_sensor = temperature_sensor
        self.temperature_path = temperature_path
        self.is_simulated = is_simulated
        self.acquisition_type = acquisition_type

        if callback:
            self.ready = self.ready_by_time

            self.task_device = {}
            for _id, chans in enumerate(self.channels):
                sorted_channels = [
                    c for c in sorted(chans, key=lambda x: chans[x])
                ]
                self.task_device[_id] = AcquisitionCallbackTask(
                    physical_channel=sorted_channels,
                    seconds_to_acquire=seconds_to_acquire,
                    rate=rate,
                    minv=minv,
                    maxv=maxv,
                    callback=callback(chans)
                )
        else:
            self.trigger_task = AcquisitionDigitalTask(
                channels=[trigger_channel],
                samples_per_channel=1
            )

            self.ready = self.ready_by_trigger

            self.task_device = {}
            for _id, chans in enumerate(self.channels):
                sorted_channels = [
                    c for c in sorted(chans, key=lambda x: chans[x])
                ]
                self.task_device[_id] = AcquisitionFiniteTask(
                    physical_channel=sorted_channels,
                    rate=rate,
                    minv=minv,
                    maxv=maxv,
                    seconds_to_acquire=seconds_to_acquire
                )

    def simulated_trigger(self):
        return 0 if not self.is_simulated else random.randint(0, 1)

    def ready(self):
        pass

    def ready_by_time(self):
        for _id, _ in enumerate(self.channels):
            self.task_device[_id].run()

    def ready_by_trigger(self):
        # check trigger
        if (
            any(map(lambda v: v > 0.0, self.trigger_task.read())) or
            self.simulated_trigger() == 1
        ):
            print('\rON ', end='')
            sys.stdout.flush()

            acq_datetime = datetime.now()

            for _id, chans in enumerate(self.channels):
                header = {
                    'acq_datetime': acq_datetime,
                    'temperature': {'5cm': None, '17cm': None},
                    'channels': len(chans),
                    'acquisition_type': self.ACQ_TYPE[self.acquisition_type]
                }

                task_dev = self.task_device[_id]

                if self.temperature_sensor:
                    # update header temperature
                    for t in [5, 17]:
                        with open('%stemp%s' % (self.temperature_path, t)) as f:
                            header['temperature']['%scm' % t] = float(f.read()) * 10

                data, acq_time = task_dev.read()

                sensors = defaultdict(dict)
                for chan_i, chan_data in data.items():
                    i_sensor = chans[chan_i]
                    for t, sensor_voltage in enumerate(chan_data):
                        # changed to return use the same baseline
                        sensor_time = acq_time[t]

                        if not sensors[i_sensor]:
                            sensors[i_sensor] = defaultdict(dict)
                        sensors[i_sensor][sensor_time] = sensor_voltage

                if self.plotting:
                    self.plot(data)

                # save the data
                AcquisitionModel(
                    header, sensors, sensor_type=self.sensor_type
                ).save()

        else:
            print('\rOFF', end='')
            sys.stdout.flush()

    def clear(self):
        """

        @return:

        """
        self.trigger_task.clear()

    def plot(self, data):
        plt.axis([0, self.samples_per_channel - 1, -2, 5.5])

        for data_sensor in data:
            plt.plot(data_sensor)

        plt.grid()
        plt.show()
