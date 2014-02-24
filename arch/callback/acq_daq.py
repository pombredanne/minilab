# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 17:04:42 2013

@author: ivan
"""
from __future__ import division, print_function
from multiprocessing import Pool
from datetime import datetime

from daq.ni.acquisition import AcquisitionTask
from arch.libs.buffer import DaqStaticBuffer
from arch.libs.segmentation import SegmentStaticTask
from arch.libs.save import save_acquisition_data
from arch.libs.util import (
    extract_devices, extract_all_channels, extract_analog_channels
)
from gui.plotter.async_chart import DaqMultiPlotter


def main(settings, dsn):
    analog_channels = extract_analog_channels(settings.DEVICES)
    all_channels = extract_all_channels(settings.DEVICES)
    devices = extract_devices(settings.DEVICES)

    devices_available_name = ['Dev5', 'Dev4']
    sensor_types_available = ['polymer', 'ceramic']

    sensors_available = {
        key: settings.DEVICES[key] for key in sensor_types_available
    }

    chunk = 2000
    samples_to_save = 15000
    limit_per_channel = samples_to_save*100

    def callback1(dev_name):
        def _cb(interval, data):
            DaqStaticBuffer.append(data)

        return _cb

    def callback2(dev_name):
        pool = Pool(processes=20)

        def _cb(interval, data):
            DaqStaticBuffer.append(data)

            segmented_data = SegmentStaticTask.search(DaqStaticBuffer)

            if segmented_data:
                print('Segmented at %s' % (datetime.now()))
                for sensor_type, sensors_data in segmented_data.items():
                    pool.apply_async(
                        save_acquisition_data,
                        args=(
                            {sensor_type: sensors_data},
                            analog_channels,
                            sensors_available, {}, dsn, 'mswim'
                        )
                    )
                #DaqMultiPlotter.send_data(segmented_data)
                #DaqMultiPlotter.show()
        return _cb

    DaqStaticBuffer.configure(all_channels, limit_per_channel)

    SegmentStaticTask.configure(
        samples_to_save, sensors_available
    )

    callback_list = {
        'Dev1': callback1,
        'Dev2': callback1,
        'Dev5': callback1,
        'Dev4': callback2
    }

    #DaqMultiPlotter.configure(samples_to_save, sensor_types_available)

    tasks = []

    for dev_name in devices_available_name:
        tasks.append(AcquisitionTask(
            device=devices[dev_name],
            acquisition_mode='callback',
            samples_per_channel=chunk,
            callback=callback_list[dev_name](dev_name)
        ))

    #DaqMultiPlotter.start()

    for task in tasks:
        task.run()

    while True:
        try:
            raw_input(
                ('Acquiring samples continuously since %s. ' +
            )
        except KeyboardInterrupt:
            break

    for task in tasks:
        task.close()

    DaqMultiPlotter.stop()

if __name__ == '__main__':
    import platform
    import sys

    # internal
    sys.path.append('../../')

    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from mswim import settings as _settings
    from mswim.libs.db import conn

    main(_settings, conn.Pool.dsn(_settings))