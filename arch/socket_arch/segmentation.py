from __future__ import print_function, division
from buffer import DaqDictRingBuffer


def segmentation_by_trigger(channels, trigger='', seconds=1, rate=2000):
    """

    """
    sampling = seconds * rate
    segmented_data = {}

    while True:
        _ = yield

        if 1 in DaqDictRingBuffer.data[trigger]:
            i = DaqDictRingBuffer.data[trigger].index(1)
            print(DaqDictRingBuffer.data)

            segmented_data = DaqDictRingBuffer.extract(i, i+sampling)

            print(segmented_data)
            print()


if __name__ == '__main__':
    from random import random

    channels = [
        dict(
            [('Dev1/ai%s' % sen, sen) for sen in range(3)] +
            [('Dev1/di0', 3)]
        )
    ]

    sorted_channels = {}
    for _id, chans in enumerate(channels):
        sorted_channels[_id] = [
            c for c in sorted(
                chans, key=lambda x: chans[x]
            )
        ]

    MAX_LINES_BUFFER = 20
    MAX_LINES = 10

    ring_buffer = DaqDictRingBuffer
    ring_buffer.configure(sorted_channels, MAX_LINES_BUFFER)

    s = segmentation_by_trigger(sorted_channels[0], 'Dev1/di0', 1, 4)
    s.next()

    daq = {
        'Dev1/di0': [0]*MAX_LINES,
        'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
    }

    ring_buffer.append(daq)
    s.send(ring_buffer.data)

    daq = {
        'Dev1/di0': [1]*1 + [0]*(MAX_LINES-1),
        'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
    }
    ring_buffer.append(daq)
    s.send(True)

    daq = {
        'Dev1/di0': [1]*1 + [0]*(MAX_LINES-1),
        'Dev1/ai0': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai1': map(lambda _: random(), range(MAX_LINES)),
        'Dev1/ai2': map(lambda _: random(), range(MAX_LINES))
    }

    ring_buffer.append(daq)
    s.send(True)