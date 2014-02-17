# -*- coding: utf-8 -*-
"""
Async module to server data from Acquisition Tasks through Ring Buffers

"""
from __future__ import print_function, division
from random import randint
from time import sleep

import asyncore
import socket
import sys
import platform

# internal
sys.path.append('../../../')
from daq.ni.acquisition import AcquisitionTask

DAQ = []

class DaqRegister(object):
    """
    Socket class to register, process and return data from Acquisition Tasks

    """
    device = ''
    daq_id = None

    def __init__(self, device={}, samples_per_channel=1000):
        """

        """
        self.device = device
        self.daq_id = len(DAQ)

        DAQ.append(AcquisitionTask(device, 'continuous', samples_per_channel))
        print('Device %s is initialized' % device['name'])

    def read(self):
        return DAQ[self.daq_id].read()
