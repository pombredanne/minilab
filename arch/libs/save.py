from labtrans.devices.daq.ni.utils import calculate_time_sequence
from collections import defaultdict
from datetime import datetime, timedelta

import numpy as np
import psycopg2
import traceback


class Acquisition(object):
    type_acquisition = {
        'quartz': 1,
        'ceramic': 2,
        'polymer': 3
    }

    def __init__(
        self, dsn, schema, samples_per_channel, rate, save_mode=1,
        sensors_settings={}, channels={}
    ):
        """
        @param save_mode: 1 to test, 2 to normal, 3 to calibration
        @type save_mode: int
        @param sensors_settings: sensors settings
        @type sensors_settings: dict
        @param channels: channels with its order to save ordered by sensor type
            Ex: {'quartz': ['Dev1/ai0', 'Dev1/ai0'], ... }
        @type channels: dict

        """
        self.conn = psycopg2.connect(dsn)
        self.schema = schema
        self.samples_per_channel = samples_per_channel
        self.time_delta = 1/rate
        self.save_mode = save_mode
        self.sensors_settings = sensors_settings
        self.channels = channels

    def save(self, data={}, weight_data={}):
        """
        Save acquisition data from dictionary

        @param data: sensors data in the follow format:
                     {'group_sensor': {'Dev#/ch#': [#.#, .... #.#]}}
        @type data: dict
        @return: True if success or False if fail
        @rtype: bool

        """
        try:
            if self.schema:
                cur = self.conn.cursor()
                cur.execute('SET search_path TO %s' % self.schema)

            for type_name in data.keys():
                acq_time = calculate_time_sequence(
                    timedelta(seconds=self.time_delta),
                    self.samples_per_channel
                )

                data[type_name]['time'] = acq_time
                chans = self.channels[type_name]

                temperature_channels = {}
                t5cm = None
                t17cm = None
                temp_chan = (
                    self.sensors_settings[type_name]['temperature_channels']
                )
                if temp_chan:
                    temperature_channels = {
                        v: k for k, v in temp_chan[0].items()
                    }

                    t5cm = data[type_name][temperature_channels[5]]
                    t17cm = data[type_name][temperature_channels[17]]

                t5cm = None if not t5cm else t5cm[0]
                t17cm = None if not t17cm else t17cm[0]

                acquisition_data = {
                    'date_time': data[type_name]['time'][0],
                    'temperature1': t5cm,
                    'temperature2': t17cm,
                    'sensor_type': self.type_acquisition[type_name],
                    'acquisition_type': self.save_mode
                }

                num_channels = len(chans)

                # added the weight data
                acquisition_data.update(weight_data)

                cur.execute(
                    ' INSERT INTO acquisition (' +
                    ' id, ' + ','.join(acquisition_data.keys()) + ')' +
                    ' VALUES(DEFAULT' +
                    (',%s' * len(acquisition_data.keys())) + ')' +
                    ' RETURNING id',
                    tuple(acquisition_data.values())
                )

                acq_id = cur.fetchone()[0]

                # Save the sensor captured data
                sql_fields = 'acquisition,acq_time,'
                sql_fields += ','.join(map(lambda n: 'sensor%s' % str(n + 1),
                                           range(num_channels)))
                sql_statement = (
                    'INSERT INTO acquisition_data_%s(%s) VALUES' % (
                        type_name, sql_fields
                    )
                )

                sql = []

                sensors = defaultdict(dict)
                for i in xrange(self.samples_per_channel):
                    sql_values = ''
                    for ch in chans:
                        sql_values += ',' + str(data[type_name][ch][i])

                    sql += [
                        sql_statement + '(' + str(acq_id) + ',\'' +
                        str(acq_time[i]) + '\'' + sql_values + ');'
                    ]

                cur.execute(''.join(sql), ())
                self.conn.commit()
                print('[II] %s saved at %s!' % (type_name, datetime.now()))

            cur.close()

        except Exception :
            print('[EE] %s' % traceback.format_exc())


        return True


def save_acquisition_data(
    data={}, channels=[], sensors_settings={},
    weight_data={}, dsn='', schema=''
):
    """
    Save acquisition data from dictionary

    @param data: sensors data in the follow format:
                 {'group_sensor': {'Dev#/ch#': [#.#, .... #.#]}}
    @type data: dict
    @param channels: channels with its order to save
    @type channels: list
    @param sensors_settings: sensors settings
    @type sensors_settings: dict

    """
    try:
        type_acquisition = {
            'quartz': 1,
            'ceramic': 2,
            'polymer': 3
        }

        conn = psycopg2.connect(dsn)

        if schema:
            cur = conn.cursor()
            cur.execute('SET search_path TO %s' % schema)

        for type_name in data.keys():
            # TODO: use variables configurations
            samples_per_channel = 15000
            acq_time = calculate_time_sequence(
                timedelta(seconds=0.0002), samples_per_channel
            )

            data[type_name]['time'] = acq_time
            chans = channels[type_name]

            temperature_channels = {}
            t5cm = None
            t17cm = None

            if sensors_settings[type_name]['temperature_channels']:
                temperature_channels = dict(
                    (v, k)
                    for k, v
                    in (
                        sensors_settings[type_name]['temperature_channels'][0]
                    ).items()
                )

                t5cm = data[type_name][temperature_channels[5]]
                t17cm = data[type_name][temperature_channels[17]]

            t5cm = None if not t5cm else t5cm[0]
            t17cm = None if not t17cm else t17cm[0]

            acquisition_data = {
                'date_time': data[type_name]['time'][0],
                'temperature1': t5cm,
                'temperature2': t17cm,
                'sensor_type': type_acquisition[type_name],
                'acquisition_type': 1  # TODO: change to a param value
            }

            num_channels = len(chans)

            # added the weight data
            acquisition_data.update(weight_data)

            cur.execute(
                ' INSERT INTO acquisition (' +
                ' id, ' + ','.join(acquisition_data.keys()) + ')' +
                ' VALUES(DEFAULT' + (',%s' * len(acquisition_data.keys())) + ')'
                ' RETURNING id',
                tuple(acquisition_data.values())
            )

            acq_id = cur.fetchone()[0]

            # Save the sensor captured data
            sql_fields = 'acquisition,acq_time,'
            sql_fields += ','.join(map(lambda n: 'sensor%s' % str(n + 1),
                                       range(num_channels)))
            sql_statement = (
                'INSERT INTO acquisition_data_%s(%s) VALUES' % (
                    type_name, sql_fields
                )
            )

            sql = []

            sensors = defaultdict(dict)
            for i in xrange(samples_per_channel):
                sql_values = ''
                for ch in chans:
                    sql_values += ',' + str(data[type_name][ch][i])

                sql += [
                    sql_statement + '(' + str(acq_id) + ',\'' +
                    str(acq_time[i]) + '\'' + sql_values + ');'
                ]

            cur.execute(''.join(sql), ())
            conn.commit()
            print('[II] %s saved at %s!' % (type_name, datetime.now()))

        cur.close()
        conn.close()
    except Exception :
        print('[EE] %s' % traceback.format_exc())


    return True