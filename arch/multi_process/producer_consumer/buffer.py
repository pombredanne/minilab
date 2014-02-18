# -*- coding: utf-8 -*-
"""

"""
from __future__ import print_function
from collections import defaultdict


class DaqBuffer(object):
    """
    Structure of the Buffer Data:

    Data in:
      [{'Dev1/ai0': [...], 'Dev1/ai1': [...], ...},
       {'Dev2/ai0': [...], 'Dev2/ai1': [...], ...},
       ...
      ]

    Data buffered:
      {'Dev1/ai0': {'polymer': [...], 'ceramic': [...], ...},
       'Dev1/ai0': {'polymer': [...], 'ceramic': [...], ...},
       ...
      }

    Data extracted:
      {'polymer': {'Dev1/ai0': [start:end], 'Dev1/ai1': [start:end], ...}}

    Data view:
      {'polymer': {'Dev1/ai0': [...], 'Dev1/ai1': [...], ...},
       'ceramic': {'Dev1/ai0': [...], 'Dev1/ai1': [...], ...}
       ...
      }

    """
    limit_per_channel = 0
    data = defaultdict(dict)
    channels = None

    def __init__(self, sensors_groups, limit_per_channel):
        """
        Prepare the buffer with the follow structure:
          {'Dev1/ai0': {'polymer': [...], 'ceramic': [...], ...},
           'Dev1/ai0': {'polymer': [...], 'ceramic': [...], ...},
           ...
          }

        @param sensors_groups: Sensors groups with its channels with the follow
            structure: {'group_name': ['channel1', 'channel2', ...], ...}
        @type sensors_groups: dict
        @param limit_per_channel: Limit data per channel
        @type limit_per_channel: int

        """
        self.limit_per_channel = limit_per_channel
        self.channels = sensors_groups

        for group_name in sensors_groups:
            for channel_name in sensors_groups[group_name]:
                self.data[channel_name][group_name] = []

    def append(self, new_data):
        """
        Append data into buffer considering the limit per channel.

        @param new_data: Data Structure:
            [{'Dev1/ai0': [...], 'Dev1/ai1': [...], ...},
             {'Dev2/ai0': [...], 'Dev2/ai1': [...], ...},
             ...]
        @type new_data: list

        """
        for item in new_data:
            for channel_name in item:
                data_size = len(item[channel_name])

                for group_name in self.data[channel_name]:
                    buffer_size = len(self.data[channel_name][group_name])

                    if buffer_size + data_size >= self.limit_per_channel:
                        i = self.limit_per_channel - buffer_size - data_size
                        self.data[channel_name][group_name][:] = (
                            self.data[channel_name][group_name][i:]
                        )
                        print('Data overwritten.')

                    self.data[channel_name][group_name] += item[channel_name]


    def extract(self, group_name, start=None, end=None):
        """
        Extract data in the range(start, end) from buffer
        filtered by group name:
        - {'polymer': {'Dev1/ai0': [start:end], 'Dev1/ai1': [start:end], ...}}

        @param group_name: Sensors group name.
        @type group_name: str
        @param start: Initial position to extract data from buffer
        @type start: int
        @param end: Final position to extract data from buffer
        @type end: int
        @return: Data in the range(start, end) from buffer
                 filtered by group name.
        @rtype: dict
        """
        result = {}

        for channel_name in self.channels[group_name]:
            result[channel_name] = (
                self.data[channel_name][group_name][start:end]
            )

            self.data[channel_name][group_name][:] = (
                self.data[channel_name][group_name][end:]
            )

        return result

    def view(self, group_name):
        """
        Return the buffer in the follow structure filtered by group_name:
        - {'Dev1/ai0': [...], 'Dev1/ai1': [...], ...}

        @param group_name: Sensors group name, example: polymer.
        @type group_name: str

        @return: Return buffer data filtered by group_name
        @rtype: dict

        """
        result = {}

        for channel_name in self.channels[group_name]:
            result[channel_name] = self.data[channel_name][group_name]

        return result


if __name__ == '__main__':
    def test1():
        # internal
        import sys
        import platform

        if platform.system() == 'Linux':
            sys.path.append('/var/www/mswim/')
        else:
            sys.path.append('c:/mswim/')

        from mswim.settings import DEVICES as SENSORS_GROUP
        from arch.libs.util import extract_devices, extract_channels

        channels = extract_channels(SENSORS_GROUP)
        limit_per_channel = 20

        x = DaqBuffer(channels, limit_per_channel)

        x.append([
            {'Dev4/ai30': [1, 2, 3, 4, 5],
             'Dev4/ai31': [6, 7, 8, 9, 0]}]
        )
        print(x.view('polymer'))

        """
        data = x.extract_data('ceramic', 0, 2)
        print('extracted data:', end='')
        print(data)
        """

        data = x.extract_data('polymer', 0, 4)
        print('extracted data:', end='')
        print(data)

        x.append([{'Dev5/ai1': [11, 12, 13, 14, 15], 'Dev5/ai2': [6, 7, 8, 9, 0]}])
        print(x.view('ceramic'))
        data = x.extract_data('ceramic', 3, 5)
        print('extracted data:')
        print(data)
        print(x.view('ceramic'))
        print(x.view('polymer'))

    test1()