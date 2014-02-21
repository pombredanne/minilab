from __future__ import division, print_function
from datetime import timedelta
from PyDAQmx import *
from PyDAQmx.DAQmxCallBack import *

from utils import calculate_time_sequence
from continuous import DigitalContinuousTask

import numpy as np


class CallbackTask(Task):
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
    digital_task = None

    def __init__(
        self,
        physical_channels=[],
        digital_physical_channels=[],
        rate=1000.,
        minv=(-5.0),
        maxv=5.0,
        samples_per_channel=1000,
        external_callback=()
    ):
        """

        """
        Task.__init__(self)

        self.physical_channels = physical_channels
        self.rate = rate

        self.samples_per_channel = samples_per_channel
        self.number_of_channels = len(physical_channels)
        self.buffer_size = self.samples_per_channel * self.number_of_channels

        # w/ calibration
        self.buffer_daq_size = int(self.buffer_size * self.rate/10)

        self.external_callback = external_callback

        self.minv = minv
        self.maxv = maxv

        self.CreateAIVoltageChan(
            ','.join(physical_channels), "", DAQmx_Val_RSE,
            minv, maxv, DAQmx_Val_Volts, None
        )

        # scaling the buffer size
        # DAQmxCfgInputBuffer(self.taskHandle, self.bufferSize)

        self.CfgSampClkTiming(
            'OnboardClock', rate, DAQmx_Val_Rising,
            DAQmx_Val_ContSamps, self.buffer_daq_size
        )

        self.AutoRegisterEveryNSamplesEvent(
            DAQmx_Val_Acquired_Into_Buffer, self.samples_per_channel, 0
        )
        self.AutoRegisterDoneEvent(0)

        if digital_physical_channels:
            self.digital_task = DigitalContinuousTask(
                digital_physical_channels, self.samples_per_channel
            )

    def bind(self, callback):
        self.external_callback = callback

    def prepare_data(self, data):
        """
        @return: data acquisitions, time of each acquisition
        """
        return dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channels)
        ])

    def EveryNCallback(self):
        read = int32()
        data = np.zeros(self.buffer_size)

        self.ReadAnalogF64(
            self.samples_per_channel, 10.0, DAQmx_Val_GroupByChannel,
            data, data.size, byref(read), None
        )

        data = self.prepare_data(data)

        timing = calculate_time_sequence(
            timedelta(seconds=1/self.rate),
            self.samples_per_channel)

        if self.digital_task:
            data.update(self.digital_task.read())

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

        if self.digital_task:
            self.digital_task.close()

        print('Acquisition stopped')


if __name__ == '__main__':
    import sys
    import platform

    # internal
    sys.path.append('../../')
    from arch.socket_arch.util import extract_devices
    from gui.plotter.async_chart import DaqMultiPlotter

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim.settings import DEVICES

    device = extract_devices(DEVICES)['Dev5']
    device2 = extract_devices(DEVICES)['Dev4']
    daq_chunk = 1000

    DaqMultiPlotter.configure(daq_chunk, ['Dev5', 'Dev4'])

    def internal_callback1(interval, data):
        DaqMultiPlotter.send_data({'Dev5': data})

    def internal_callback2(interval, data):
        DaqMultiPlotter.send_data({'Dev4': data})
        DaqMultiPlotter.show()

    callback_task = CallbackTask(
        physical_channels=device['analog'],
        digital_physical_channels=device['digital'],
        rate=device['rate'],
        minv=device['minv'],
        maxv=device['maxv'],
        samples_per_channel=daq_chunk,
        external_callback=internal_callback1
    )

    callback_task2 = CallbackTask(
        physical_channels=device2['analog'],
        digital_physical_channels=device2['digital'],
        rate=device2['rate'],
        minv=device2['minv'],
        maxv=device2['maxv'],
        samples_per_channel=daq_chunk,
        external_callback=internal_callback2
    )

    DaqMultiPlotter.start()

    callback_task.run()
    callback_task2.run()

    while True:
        try:
            raw_input(
                'Acquiring samples continuously. Press CTRL + C to interrupt\n'
            )
        except KeyboardInterrupt:
            break

    callback_task.stop()
    callback_task2.stop()
    DaqMultiPlotter.stop()