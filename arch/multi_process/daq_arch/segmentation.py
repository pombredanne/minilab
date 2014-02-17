# -*- coding: utf-8 -*-
from __future__ import print_function, division
from acquisition.util.buffer import DaqDictRingBuffer
from collections import defaultdict

CALLBACK = []

class SegmentedByTrigger(object):
    """

    """
    buffer_name=''
    channels=[]
    trigger=''
    chunk=0
    ring_buffer=None
    callback=None

    def __init__(
        self,
        buffer_name='',
        channels=[],
        sensors_group={},
        trigger='',
        chunk=15000,
        callback=(lambda x: x)
    ):
        """

        """
        self.callback_id = len(CALLBACK)
        self.buffer_name = buffer_name
        self.channels = channels
        self.trigger = trigger
        self.chunk = chunk
        self.sensors_group = sensors_group
        CALLBACK.append(callback)

    def check(self, data):
        """

        """
        if 1 in data[self.trigger]:
            i = data[self.trigger].index(1)

            if i is None or i + self.chunk >= len(data[self.trigger]):
                return self.buffer_name, None

            return self.buffer_name, i

    def callback(self, segmented_data, sensors_group):
        CALLBACK[self.callback_id](
            self.buffer_name, segmented_data, sensors_group
        )