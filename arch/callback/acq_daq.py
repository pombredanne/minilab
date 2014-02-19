# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:04:42 2013

@author: ivan
"""
from __future__ import division, print_function
from daq.ni.acquisition import AcquisitionTask
from datetime import datetime, timedelta
from matplotlib import pyplot as plt


def main(settings):
    # REMOVE GROUPS WITH ACQUISITION EQUAL TO FALSE
    _sensors_settings = {}
    for i in settings.DEVICES:
        if settings.DEVICES[i]['acquisition_mode']:
            _sensors_settings[i] = settings.DEVICES[i]

            task_dev1 = AcquisitionTask(device, 'continuous', samples_per_channel)
            task_dev2 = AcquisitionCallbackTask(
                physicalChannel=dev2, rate=5000., minv=-5.0, maxv=5.0, pid=2
            )

    task_dev1.run()
    task_dev2.run()

    plt.ion()
    plt.show()

    while True:
        try:
            raw_input('Acquiring samples continuously. Press CTRL + C to interrupt\n')
        except KeyboardInterrupt:
            break

    task_dev1.stop()
    task_dev2.stop()

    plt.ioff()

if __name__ == '__main__':
    # internal
    import sys
    sys.path.append('/var/www/mswim/')

    from mswim import settings

    main(settings)