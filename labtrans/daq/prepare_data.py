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
sys.path.insert(0, '/var/www/mswim/')

# mswim packages
from mswim import settings
from mswim.libs.db import conn as db
from mswim.apps.acquisition.models import AcquisitionModel


def calc_time(delta_t, N):
    timestamp = [datetime.now()]

    def next_time(stamp):
        _ts = stamp[0]
        stamp[0] += delta_t
        return _ts

    return [next_time(timestamp) for _ in range(N)]


def test():
    db.Pool.connect()
    data_pickle = pickle.load(open('data.pic', 'rb'))

    DEVICES = {}

    _channels = [dict([('Dev2/ai%s' % sen, sen) for sen in range(16)])]
    DEVICES['ceramic'] = {
        'trigger': 'Dev2/port0/line0',
        'channels': _channels,
        'sensor_type': 2,
        'temperature_sensor': False,
        'rate':5000,
        'minv':-10,
        'maxv':10
    }

    for chans in DEVICES['ceramic']['channels']:
        header = {
            'acq_datetime': datetime.now(),
            'temperature': {'5cm': None, '17cm': None},
            'channels': len(chans)
        }

        data, acq_time = data_pickle, calc_time(timedelta(seconds=1/5000), 10000)

        sensors = defaultdict(dict)
        for chan_i, chan_data in data.items():
            i_sensor = str(chans[chan_i])
            for t, sensor_voltage in enumerate(chan_data):
                # changed to return use the same baseline
                sensor_time = acq_time[t]

                if not sensors[i_sensor]:
                    sensors[i_sensor] = defaultdict(dict)
                sensors[i_sensor][sensor_time] = sensor_voltage
                print(sensor_voltage)

        # print(count_0)  # 4 sensores
        # print(count_1)  # 10000 puntos para cada sensor
        # print(sensors)
        # exit()
        # save the data
        acq = AcquisitionModel(
            header, sensors, sensor_type=2
        )

        plot(acq.data.dict())


def test():
    db.Pool.connect()

    acq = AcquisitionModel.load('1010')
    plot(acq.data.dict())


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


if __name__ == '__main__':
    test()