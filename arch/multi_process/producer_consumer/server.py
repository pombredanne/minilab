# -*- coding: utf-8 -*-
"""
Module to server access to Acquisition Tasks

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


class DaqRegister(object):
    """
    Socket class to register, process and return data from Acquisition Tasks

    """
    device = ''
    name = None
    daq = None

    def __init__(self, device={}, samples_per_channel=1000):
        """

        """
        self.device = device
        self.name = device['name']

        self.daq = AcquisitionTask(device, 'continuous', samples_per_channel)
        print('Device %s is initialized' % device['name'])

    def read(self):
        return self.daq.read()
