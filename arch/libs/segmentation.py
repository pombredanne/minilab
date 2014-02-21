# -*- coding: utf-8 -*-
from __future__ import print_function, division
from arch.libs.buffer import DaqStaticBuffer, DaqBuffer


class SegmentTask(object):
    chunk = None

    def __init__(self, chunk=0, sensors=None):
        self.chunk = chunk
        self.sensors = sensors

    def __call__(self, daq_buffer):
        result = {}
        for sensor_id, sensor in self.sensors.items():
            # ex. sensor_id: polymer, ceramic, etc
            trigger_data = daq_buffer.view(sensor_id)[
                sensor['trigger']
            ]

            data_size = len(trigger_data)

            try:
                i = trigger_data.index(1)
            except ValueError:
                return None

            if i + self.chunk > data_size:
                return None

            result[sensor_id] = daq_buffer.extract(sensor_id, i, i+self.chunk)
        return result


class SegmentStaticTask(object):
    chunk = None
    censors = {}

    @classmethod
    def configure(cls, chunk=0, sensors=None):
        """
        Configure data structure to receive data

        @param chunk: chunk of segmented data
        @type chunk: int
        @param sensors: sensors dictionary grouped by type of sensors
        @type sensors: dict

        """
        cls.chunk = chunk
        cls.sensors = sensors

    @classmethod
    def search(cls, daq_buffer):
        """
        Search by trigger signal to segment data

        @param daq_buffer: DAQ Buffer reference
        @type daq_buffer: DaqStaticBuffer
        @return: Segmented data from all sensors type
        @rtype: dict

        """
        result = {}
        for sensor_id, sensor in cls.sensors.items():
            if 'trigger' not in sensor or not sensor['trigger']:
                continue
            # ex. sensor_id: polymer, ceramic, etc
            trigger_data = daq_buffer.view(sensor_id)[
                sensor['trigger']
            ]

            data_size = len(trigger_data)

            try:
                i = trigger_data.index(1)
            except ValueError:
                continue

            if (
                i + cls.chunk > data_size or
                not daq_buffer.check_min_size(sensor_id, i, i+cls.chunk)
            ):
                continue

            result[sensor_id] = daq_buffer.extract(sensor_id, i, i+cls.chunk)
        return result