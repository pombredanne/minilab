# -*- coding: utf-8 -*-
from __future__ import print_function
from PyDAQmx import *
from datetime import datetime

import traceback
import sys
import numpy
import numpy as np
import sys

# internal
from acq_finite_time import AcquisitionFiniteTask
from prepare_acquisition_data import get_acquisition_data
from raw_data import save_file

sys.path.insert(0, '/var/www/mswim')
from mswim import settings


class WimTask():
    """

    """

    digital_task = None
    analogic_task = None
    channel = None
    read = None
    bytes_per_samp = None
    samples_per_channel = None

    def __init__(self):
        """

        @return:
        """
        self.configure()

    def configure(self):
        """

        @return:
        """

        self.digital_task = TaskHandle()


        self.channel = "Dev2/port0/line0"

        self.read = int32()
        self.bytes_per_samp = int32()
        self.samples_per_channel = 1

        self.dev1 = ['Dev1/ai%s' % line for line in range(0, 4)]
        self.dev2 = ['Dev2/ai%s' % line for line in range(0, 4)]


    def ready(self, device):
        raw_input('Press ENTER to acquire data.')


        #print('\rON ', end='')
        #sys.stdout.flush()

        print('ON')

        task_dev = AcquisitionFiniteTask(
            physical_channel=device['channels'], rate=device['rate'],
            minv=device['minv'], maxv=device['maxv'],
            time_to_acquire=9
        )

        data = task_dev.read()

        acq = get_acquisition_data(data, device)
        save_file(
            acq, '/tmp/wim_raw_data_%s.txt' %
                 (str(datetime.now()).replace(' ', '-'))
        )

        task_dev.plot(data)

        del task_dev

        #print('\rOFF', end='')
        #sys.stdout.flush()
        print('OFF')


def main():
    task = WimTask()

    device = settings.DEVICES[sys.argv[1]]

    while True:
        try:
            task.ready(device)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print('Fatal error: %s' % traceback.format_exc())
            break

if __name__ == '__name__':
    main()