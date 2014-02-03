from __future__ import print_function
from random import random, randint
from collections import defaultdict
import numpy as np


def digital_generator():
    return randint(0, 1)


def analog_generator():
    return random()


def gen_data(sensors, size=6500):
    """

    """
    cache = []

    while True:
        cache[:] = []
        count = 0
        while count < size:
            cache += [
                random() for _ in sorted(sensors, key=lambda i: sensors[i])
            ]
            count += 1

        yield cache


class AcquisitionTask():
    """

    """
    ACQ_TYPE = {
        'test': 2,
        'calibration': 3,
        'statistic': 1
    }

    analog_task = None
    digital_task = None

    device = None

    def __init__(self, device={}, acquisition_mode=''):
        """

        @return:

        """
        self.device = device

        self.digital_task = GeneratorDigitalTask(
            physical_channels=device['digital'],
            rate=device['rate']
        )

        self.analog_task = GeneratorAnalogTask(
            physical_channels=device['analog'],
            rate=device['rate'],
            minv=device['minv'],
            maxv=device['maxv'],
            seconds_to_acquire=device['seconds_to_acquire']
        )

    def read(self):
        signals = self.read_analog()
        signals.update(self.read_digital())
        return signals

    def read_analog(self):
        data = self.analog_task.read()

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            for i, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                if not sensors[chan_i]:
                    sensors[chan_i] = []
                sensors[chan_i] += [sensor_voltage]
        return sensors

    def read_digital(self):
        if not self.digital_task.physical_channels:
            return {}

        data = self.digital_task.read()

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            for i, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                if not sensors[chan_i]:
                    sensors[chan_i] = []
                sensors[chan_i] += [sensor_voltage]
        return sensors

    def close(self):
        """

        @return:

        """
        pass


class GeneratorAnalogTask():
    """

    """
    task = None
    physical_channels = None
    seconds_to_acquire = None
    rate = None
    samples_per_channel = None
    number_of_channels = None
    buffer_size = None
    minv = None
    maxv = None

    def __init__(
        self,
        physical_channels=[],
        rate=1.0,
        minv=(-5.0),
        maxv=5.0,
        seconds_to_acquire=3
    ):
        """

        """
        self.physical_channels = physical_channels
        self.seconds_to_acquire = seconds_to_acquire
        self.rate = rate

        self.samples_per_channel = int(self.rate * 1)  # 2 second sampled
        self.number_of_channels = len(physical_channels)
        self.buffer_size = self.samples_per_channel * self.number_of_channels

        self.minv = minv
        self.maxv = maxv

    def read(self):
        """
        @return: data acquisitions, time of each acquisition
        """
        data = self._read()

        return dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channels)
        ])

    def _read(self):
        """

        """
        data = np.zeros((self.buffer_size,), dtype=np.float64)

        for x in xrange(self.buffer_size):
            data[x] = analog_generator()

        return data

    def close(self):
        print('')
        print('Clearing ...')
        try:
            print('\nTask stopped')
        except:
            pass

        try:
            print('Quit')
        except:
            pass
        return


class GeneratorDigitalTask(object):
    """

    """
    task = None
    physical_channels = None
    read_int32 = None
    bytes_per_samp_int32 = None
    samples_per_channel = None

    def __init__(
        self,
        physical_channels,
        rate
    ):
        self.physical_channels = physical_channels
        self.rate = rate
        self.samples_per_channel = int(self.rate * 1)  # 2 second sampled
        self.buffer = self.samples_per_channel * len(physical_channels)

    def read(self):
        """
        @return: data acquisitions, time of each acquisition
        """
        if not self.physical_channels:
            return {}

        data = self._read()

        result = dict([
            (name, data[i * self.samples_per_channel:
                        (i + 1) * self.samples_per_channel])
            for i, name in enumerate(self.physical_channels)
        ])
        return result

    def _read(self):
        """

        """
        data = np.zeros((self.samples_per_channel,), dtype=np.uint8)
        for x in xrange(self.samples_per_channel):
            data[x] = digital_generator()

        return data

    def close(self):
        """

        @return:

        """
        if not self.physical_channels:
            return

        print('\nStopping ... ', end='')
        print('OK. Quit.')
        return