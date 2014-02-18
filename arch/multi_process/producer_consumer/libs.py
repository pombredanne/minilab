# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict
import psutil
import os


def memory_usage():
    """
    Return memory usage in MB unity.
    """
    process = psutil.Process(os.getpid())
    return process.get_memory_info()[0] / float(2 ** 20)