from __future__ import print_function, division
from collections import defaultdict


class Weigh(object):
    """

    """
    @classmethod
    def calculate(cls, data):
        """
        Coroutine to segmentation data by trigger

        """
        weight = defaultdict(dict)
        for group_name in data:
            for channel in data[group_name]:
                weight[group_name][channel] = 0.

        return weight

