# -*- coding: utf8 -*-
"""
Writes multiple floating-point samples to a task that contains
one or more analog output channels.

Note: If you configured timing for your task, your write is considered a
buffered write. Buffered writes require a minimum buffer size of 2 samples.
If you do not configure the buffer size using DAQmxCfgOutputBuffer,
NI-DAQmx automatically configures the buffer when you configure sample timing.
If you attempt to write one sample for a buffered write without configuring
the buffer, you will receive an error.

"""
from __future__ import print_function
from reportlab.platypus.paraparser import _num
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from collections import defaultdict
from time import sleep

import numpy as np
import time as time
import sys
import platform

# internal
if platform.system() == 'Linux':
    sys.path.append('/var/www/mswim/')
else:
    sys.path.append('c:/mswim/')

from mswim import settings

sys.path.append('../../')
from database.psql.db import DB


def simulate_daq(sampling_per_channel=15000):
    """

    """
    chan = yield
    num_channels = len(chan)

    conn = DB.connect(settings)

    # consulta adquisición
    cursor_acq = DB.cursor()

    sql = '''
    SELECT
      id,
      TO_CHAR(date_time, 'YYYY-MM-DD HH24:MI:SS') as date_time
      FROM acquisition
      where id >10
    '''
    cursor_acq.execute(sql, ())

    aquisitions = cursor_acq.fetchall()
    cursor_acq.close()

    list_time = np.arange(0, sampling_per_channel, 1)

    counter = 0

    sensors_db = ', '.join(
        map(lambda i: 'sensor%s' % (i+1), xrange(num_channels))
    )

    yield

    window = [[0.0]] * num_channels

    size = 1000

    while True:
        for acq in aquisitions:
            # consulta adquisición de señal
            sql = '''
            SELECT %s
            FROM acquisition_data_quartz where acquisition=%s
            ''' % (sensors_db, '%s')

            cursor_data = DB.cursor()
            cursor_data.execute(sql, (acq.id,))

            data = defaultdict(list)

            data_signal = cursor_data.fetchall()
            cursor_data.close()

            if len(data_signal) == 0:
                continue

            for ds in data_signal:
                for i in xrange(num_channels):
                    window[i] = window[i] + [eval('ds.sensor%s' % (i+1))]

                if len(window[0]) == size:
                    yield window
                    window = [[0.0]] * num_channels


if __name__ == '__main__':
    channels = ['Dev1/ao0', 'Dev1/ao1', 'Dev1/ao2', 'Dev1/ao3']
    s = simulate_daq()
    s.next()
    s.send(channels)
    print(s.next())