from __future__ import print_function, division
from buffer import DaqDictRingBuffer
from collections import defaultdict


class SegmentationSignal(object):
    """

    """
    @classmethod
    def by_trigger(
        cls, buffer_name='', channels=[], trigger='', chunk=15000,
        ring_buffer=None, callback=(lambda x: x)
    ):
        """
        Coroutine to segmentation data by trigger

        """
        segmented_data = {}

        while True:
            yield True
            segmented_data.clear()

            if 1 in ring_buffer.data[buffer_name][trigger]:
                i = ring_buffer.data[buffer_name][trigger].index(1)

                segmented_data = ring_buffer.extract(
                    buffer_name=buffer_name, chunk=i+chunk, start_index=i
                )

            if segmented_data:
                callback(segmented_data)


class SegmentedByTrigger(object):
    """

    """
    def __init__(
        self, buffer_name='', channels=[], trigger='', chunk=15000,
        ring_buffer=None, callback=(lambda x: x)
    ):
        self.trigger = SegmentationSignal.by_trigger(
            buffer_name=buffer_name,
            channels=channels,
            trigger=trigger,
            chunk=chunk,
            ring_buffer=ring_buffer,
            callback=callback
        )
        self.trigger.next()

    def read(self):
        self.trigger.next()


if __name__ == '__main__':
    def test1():
        from random import random

        channels = [
            dict(
                [('Dev1/ai%s' % sen, sen) for sen in range(3)] +
                [('Dev1/di0', 3)]
            )
        ]

        sorted_channels = []
        for chans in channels:
            sorted_channels += [
                c[0] for c in sorted(
                    chans.items(), key=lambda x: x[1]
                )
            ]

        MAX_LINES_BUFFER = 20
        MAX_LINES = 10
        buffer_name = 'Dev1'

        ring_buffer = DaqDictRingBuffer
        ring_buffer.configure(
            MAX_LINES_BUFFER, None, overwritten_exception=False
        )
        ring_buffer.bind(buffer_name, sorted_channels)

        s = SegmentationSignal.by_trigger(
            channels=sorted_channels,
            trigger='Dev1/di0',
            chunk=5,
            ring_buffer=ring_buffer,
            callback=print
        )
        s.next()

        daq = {
            'Dev1/di0': [1]*1 + [0]*(MAX_LINES-1),
            'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
        }

        ring_buffer.append(buffer_name, daq)
        s.next()

        daq = {
            'Dev1/di0': [1]*1 + [0]*(MAX_LINES-1),
            'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
        }
        ring_buffer.append(buffer_name, daq)
        s.next()

        daq = {
            'Dev1/di0': [1]*1 + [0]*(MAX_LINES-1),
            'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
            'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
        }

        ring_buffer.append(buffer_name, daq)
        ring_buffer.append(buffer_name, daq)
        ring_buffer.append(buffer_name, daq)
        ring_buffer.append(buffer_name, daq)
        ring_buffer.append(buffer_name, daq)
        s.next()

    test1()