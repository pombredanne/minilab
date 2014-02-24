# -*- coding: utf-8 -*-
from __future__ import print_function
from collections import defaultdict


def extract_devices(sensors):
    _DEVICE = defaultdict(dict)

    for sensors_group in sensors:
        if (
            not sensors[sensors_group]['acquisition_mode'] and
            not sensors_group == 'temperature'
        ):
            continue
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


def extract_analog_channels(sensors):
    _SENSORS_GROUPS = defaultdict(dict)

    for sensors_name in sensors:
        if not sensors[sensors_name]['acquisition_mode']:
            continue

        # analog channels
        for item in sensors[sensors_name]['channels']:
            for channel in sorted(item, key=lambda i: item[i]):
                if not _SENSORS_GROUPS[sensors_name]:
                    _SENSORS_GROUPS[sensors_name] = []
                _SENSORS_GROUPS[sensors_name] += [channel]

    return _SENSORS_GROUPS


def extract_all_channels(sensors):
    _SENSORS_GROUPS = defaultdict(dict)

    for sensors_name in sensors:
        if not sensors[sensors_name]['acquisition_mode']:
            continue

        # analog channels
        for item in sensors[sensors_name]['channels']:
            for channel in sorted(item, key=lambda i: item[i]):
                if not _SENSORS_GROUPS[sensors_name]:
                    _SENSORS_GROUPS[sensors_name] = []
                _SENSORS_GROUPS[sensors_name] += [channel]

        # digital channels
        if sensors[sensors_name]['trigger']:
            _SENSORS_GROUPS[sensors_name] += [sensors[sensors_name]['trigger']]

        if (
            sensors[sensors_name]['temperature_channels']
        ):
            for channels in sensors[sensors_name]['temperature_channels']:
                for channel in channels:
                    _SENSORS_GROUPS[sensors_name] += [channel]

    return _SENSORS_GROUPS