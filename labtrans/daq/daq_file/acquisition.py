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

sys.path.insert(0, 'c:/mswim/')
from mswim import settings
from mswim.libs.db import conn


class WimTask(object):
    """

    """
    @classmethod
    def ready(cls, device, time_to_acquire=3):
        """

        """
        raw_input('Press ENTER to acquire data.')

        #print('\rON ', end='')
        #sys.stdout.flush()

        channels = [
            c for c in sorted(
                device['channels'][0], key=lambda x: device['channels'][0][x]
            )
        ]

        print('ON')

        task_dev = AcquisitionFiniteTask(
            physical_channel=channels, rate=device['rate'],
            minv=device['minv'], maxv=device['maxv'],
            time_to_acquire=time_to_acquire
        )

        data = task_dev.read()

        acq = get_acquisition_data(data, device, time_to_acquire)
        save_file(
            acq, 'c:/tmp/wim_raw_data_%s.txt' %
                 (str(datetime.now())[:19].replace(' ', '_').replace(':', '_'))
        )

        task_dev.plot(data)

        del task_dev

        #print('\rOFF', end='')
        #sys.stdout.flush()
        print('OFF')


def main():
    print('Starting ...')
    conn.Pool.connect()

    device = settings.DEVICES['ceramic']

    while True:
        try:
            WimTask.ready(device, time_to_acquire=9)
        except KeyboardInterrupt:
            print('KeyboardInterrupt')
            break
        except Exception as e:
            print('Fatal error: %s' % traceback.format_exc())
            break


if __name__ == '__main__':
    main()