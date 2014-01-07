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
from psycopg2 import extras
from matplotlib import pyplot as plt
from matplotlib.ticker import EngFormatter
from collections import defaultdict
from time import sleep
from PyDAQmx import *

import settings
import numpy as np
import time as time
import sys

sys.path.append('../')
from db.connection import db_connect, db_cursor


def configure(physical_channels, buffer, sampling=15000, rate=100):
    # DAQmxResetDevice(physical_channels[0].split('/')[0])
    task = TaskHandle()

    # DAQmx Configure Code
    DAQmxCreateTask('', byref(task))

    DAQmxCreateAOVoltageChan(
        task,
        ','.join(physical_channels),
        '',
        -5.0,
        5.0,
        DAQmx_Val_Volts,
        None
    )

    DAQmxCfgSampClkTiming(
        task,
        '',
        rate,
        DAQmx_Val_Rising,
        DAQmx_Val_FiniteSamps,
        sampling
    )

    return task


def generador_daq(chan=['Dev1/ao0'], sampling_per_channel=15000, rate=5000):
    """

    """
    buffer = int32()
    task = configure(chan, buffer, sampling_per_channel, rate)
    num_channels = len(chan)

    conn = db_connect(settings)

    # consulta adquisición
    cursor_acq = db_cursor(conn, settings)

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

    #plt.ion()
    #plt.show()

    list_time = np.arange(0, sampling_per_channel, 1)

    counter = 0

    print('Writing ...')

    while True:
        for acq in aquisitions:
            # consulta adquisición de señal
            sql = '''
            SELECT sensor1, sensor2, sensor3, sensor4
            FROM acquisition_data_quartz where acquisition=%s
            '''

            cursor_data = db_cursor(conn, settings)
            cursor_data.execute(sql, (acq.id,))

            data = defaultdict(list)

            data_signal = cursor_data.fetchall()
            cursor_data.close()

            if len(data_signal) == 0:
                continue

            window = [[0.0]] * 4

            for ds in data_signal:
                # int32 DAQmxWriteAnalogScalarF64 (
                #    TaskHandle taskHandle,
                #    bool32 autoStart,
                #    float64 timeout,
                #    float64 value,
                #    bool32 *reserved);

                window[0] = window[0] + [ds.sensor1]
                window[1] = window[1] + [ds.sensor2]
                window[2] = window[2] + [ds.sensor3]
                window[3] = window[3] + [ds.sensor4]

            '''
            #plt.clf()
            ax = plt.subplot(111)
            #ax.set_xscale('log')
            formatter = EngFormatter(unit='t', places=1)
            ax.xaxis.set_major_formatter(formatter)

            ax.plot(window[0])
            #ax.plot(list_time, window[1])
            #ax.plot(list_time, window[2])
            #ax.plot(list_time, window[3])

            plt.grid()
            plt.show()
            '''

            try:
                DAQmxWaitUntilTaskDone(task, 10.0)
                DAQmxStopTask(task)
            except:
                pass

            DAQmxWriteAnalogF64(
                task,
                sampling_per_channel,
                True,
                10.0,
                DAQmx_Val_GroupByChannel,
                np.array(
                    window[0] +
                    window[1] +
                    window[2] +
                    window[3]),
                byref(buffer),
                None
            )


if __name__ == '__main__':
    generador_daq(['Dev1/ao0', 'Dev1/ao1', 'Dev1/ao2', 'Dev1/ao3'])