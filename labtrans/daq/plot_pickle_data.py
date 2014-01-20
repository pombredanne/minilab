# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 16:11:48 2013

@author: ivan
"""
from __future__ import print_function, division
from PyDAQmx import *
from PyDAQmx.DAQmxFunctions import *
from PyDAQmx.DAQmxConstants import *
from matplotlib import pyplot as plt

import numpy as np
import time
import pickle


def plot(data):
    plt.axis([0, 10000-1, -2, 5.5])

    plt.plot(data['Dev2/ai0'])
    plt.plot(data['Dev2/ai1'])
    plt.plot(data['Dev2/ai2'])
    plt.plot(data['Dev2/ai3'])

    plt.grid()
    plt.show()


def test():
    plot(pickle.load(open('data.pic', 'rb')))

    return


if __name__ == '__main__':
    test()