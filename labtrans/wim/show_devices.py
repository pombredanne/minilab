# -*- coding: utf-8 -*-
from collections import defaultdict
import sys
import platform

# internal
if platform.system() == 'Linux':
    sys.path.append('/var/www/mswim/')
else:
    sys.path.append('c:/mswim/')

from mswim.settings import DEVICES as DEV

_DEVICE = defaultdict(dict)

for sensors_group in DEV:
    # analog channels
    for item in DEV[sensors_group]['channels']:
        for channel in sorted(item, key=lambda i: item[i]):
            device_name = channel.split('/')[0]
            if not _DEVICE[device_name]:
                _DEVICE[device_name] = {
                    'analog': [],
                    'digital': [],
                    'rate': DEV[sensors_group]['rate'],
                    'minv': DEV[sensors_group]['minv'],
                    'maxv': DEV[sensors_group]['maxv'],
                    'seconds_to_acquire': DEV[sensors_group]['seconds_to_acquire']
                }

            _DEVICE[device_name]['analog'] += [channel]

    # digital channels
    if not DEV[sensors_group]['trigger']:
        continue

    trigger_name = DEV[sensors_group]['trigger']
    device_name = trigger_name.split('/')[0]
    if not _DEVICE[device_name]:
        _DEVICE[device_name] = {
            'analog': [],
            'digital': [],
            'rate': 1000,
            'minv': -10,
            'maxv': +10,
            'seconds_to_acquire': 1.0
        }

    _DEVICE[device_name]['digital'] += [trigger_name]

print(_DEVICE)