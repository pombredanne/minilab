# -*- coding: utf-8 -*-
from __future__ import print_function, division
from acquisition.util.buffer import DaqDictRingBuffer
from collections import defaultdict

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