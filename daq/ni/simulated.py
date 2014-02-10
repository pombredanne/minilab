# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""
from __future__ import print_function, division
from random import random, randint, shuffle
from collections import defaultdict

import numpy as np


def digital_wave(channels=[], samples_per_channel=1000):
    t = [0]*(samples_per_channel-100) + [1]*100

    result = []
    while True:
        for position in xrange(0, samples_per_channel, 1000):
            result[:] = []
            for k, ch in enumerate(channels):
                shuffle(t)
                result += list(t)

            yield result


def sin_wave(channels=[], samples_per_channel=1000):
    t = np.linspace(0, 1, samples_per_channel)

    data_size = t.size

    result = []
    while True:
        for position in xrange(0, samples_per_channel, 1):
            amplitude = randint(1, 10)  # Amplitude
            result[:] = []
            for k, ch in enumerate(channels):
                data = list(t[position:data_size]) + list(t[0:position])
                data = np.sin(2 * np.pi * np.array(data) + k) * amplitude
                result += list(data)

            yield result


def triangle_wave(channels=[], samples_per_channel=1000):
    t = np.linspace(0, 1, samples_per_channel)
    number_of_channels = len(channels)
    data_size = t.size
    amplitude = 10  # Amplitude

    result = []
    while True:
        for position in xrange(0, samples_per_channel, 10):
            result[:] = []
            for k, ch in enumerate(channels):
                data = list(t[position:data_size]) + list(t[0:position])
                data = np.array(data) + (k / number_of_channels) * amplitude
                result += list(data)

            yield result


class AcquisitionSimulatedTask():
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

    def __init__(self, device={}, acquisition_mode='', samples_per_channel=1):
        """

        @return:

        """
        self.device = device

        self.digital_task = DigitalSimulatedTask(
            physical_channels=device['digital'],
            rate=device['rate'],
            samples_per_channel=samples_per_channel
        )

        self.analog_task = AnalogSimulatedTask(
            physical_channels=device['analog'],
            rate=device['rate'],
            minv=device['minv'],
            maxv=device['maxv'],
            seconds_to_acquire=device['seconds_to_acquire'],
            samples_per_channel=samples_per_channel
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


class AnalogSimulatedTask():
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

    def __init__(
        self,
        physical_channels=[],
        rate=1.0,
        minv=(-5.0),
        maxv=5.0,
        seconds_to_acquire=3,
        samples_per_channel=1000
    ):
        """

        """
        self.physical_channels = physical_channels
        self.seconds_to_acquire = seconds_to_acquire
        self.rate = rate

        self.samples_per_channel = samples_per_channel
        self.number_of_channels = len(physical_channels)
        self.buffer_size = self.samples_per_channel * self.number_of_channels
        self.buffer_daq_size = (
            self.samples_per_channel * self.number_of_channels * rate
        )

        self.minv = minv
        self.maxv = maxv

        self.analog_generator = sin_wave(
            channels=self.physical_channels,
            samples_per_channel=self.samples_per_channel
        )

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
        return self.analog_generator.next()

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


class DigitalSimulatedTask(object):
    """

    """
    task = None
    physical_channels = None
    samples_per_channel = None
    buffer_size = None
    buffer_daq_size = None
    digital_generator = None

    def __init__(
        self,
        physical_channels,
        rate=1000.,
        samples_per_channel=1000
    ):
        self.physical_channels = physical_channels
        self.rate = rate
        self.samples_per_channel = samples_per_channel
        self.buffer_size = samples_per_channel * len(physical_channels)
        self.buffer_daq_size = (
            samples_per_channel * len(physical_channels) * rate
        )

        self.digital_generator = digital_wave(
            channels=self.physical_channels,
            samples_per_channel=self.samples_per_channel
        )

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
        return self.digital_generator.next()

    def close(self):
        """

        @return:

        """
        if not self.physical_channels:
            return

        print('\nStopping ... ', end='')
        print('OK. Quit.')
        return