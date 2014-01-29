# -*- coding: utf-8 -*-
from collections import defaultdict


def extract_devices(sensors):
    _DEVICE = defaultdict(dict)

    for sensors_group in sensors:
        # analog channels
        for item in sensors[sensors_group]['channels']:
            for channel in sorted(item, key=lambda i: item[i]):
                device_name = channel.split('/')[0]
                if not _DEVICE[device_name]:
                    _DEVICE[device_name] = {
                        'name': device_name,
                        'analog': [],
                        'digital': [],
                        'rate': sensors[sensors_group]['rate'],
                        'minv': sensors[sensors_group]['minv'],
                        'maxv': sensors[sensors_group]['maxv'],
                        'seconds_to_acquire': (
                            sensors[sensors_group]['seconds_to_acquire']
                        )
                    }

                _DEVICE[device_name]['analog'] += [channel]

        # digital channels
        if not sensors[sensors_group]['trigger']:
            continue

        trigger_name = sensors[sensors_group]['trigger']
        device_name = trigger_name.split('/')[0]
        if not _DEVICE[device_name]:
            _DEVICE[device_name] = {
                'name': device_name,
                'analog': [],
                'digital': [],
                'rate': 1000,
                'minv': -10,
                'maxv': +10,
                'seconds_to_acquire': 1.0
            }

        _DEVICE[device_name]['digital'] += [trigger_name]

    return _DEVICE
