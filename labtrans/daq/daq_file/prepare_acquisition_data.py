from __future__ import division
from datetime import timedelta, datetime
from collections import defaultdict
from matplotlib.ticker import EngFormatter

import matplotlib.pyplot as plt
import pickle
import sys
from copy import deepcopy
import numpy as np

# mswim module path
sys.path.insert(0, 'c:/mswim/')

# mswim packages
from mswim.apps.acquisition.models import AcquisitionModel


def calc_time(delta_t, N):
    timestamp = [datetime.now()]

    def next_time(stamp):
        _ts = stamp[0]
        stamp[0] += delta_t
        return _ts

    return [next_time(timestamp) for _ in range(N)]


def get_acquisition_data(data, device, time_to_acquire=3):
    """

    """
    for chans in device['channels']:
        header = {
            'acq_datetime': datetime.now(),
            'temperature': {'5cm': None, '17cm': None},
            'channels': len(chans)
        }

        acq_time = calc_time(
            timedelta(seconds=1/device['rate']),
            device['rate'] * time_to_acquire
        )

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            i_sensor = str(chans[chan_i])
            for t, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                sensor_time = acq_time[t]

                if not sensors[i_sensor]:
                    sensors[i_sensor] = defaultdict(dict)
                sensors[i_sensor][sensor_time] = sensor_voltage
                #print(sensor_voltage)

        return AcquisitionModel(
            header, sensors, sensor_type=2
        )


def plot(dados):
    formatter = EngFormatter(unit='s', places=1)

    # Analisa os sensores
    for sensor in dados:
        ax = plt.subplot(111)
        ax.xaxis.set_major_formatter(formatter)
        xs = []
        ys = []

        "Analisa os tempos do sensor"
        for tempo in sorted(dados[sensor].keys()):
            xs.append(tempo)
            ys.append(dados[sensor][tempo])

        ax.plot(xs, ys)
    plt.show()
