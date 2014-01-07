# -*- coding: utf8 -*-
from __future__ import print_function
from psycopg2 import extras
from collections import defaultdict
from dsp import snr
import numpy as np
import psycopg2
import settings
from itertools import product

def db_cursor(connection):
    cur = connection.cursor()
    db_conf = settings.DATABASE

    if 'SCHEMA' in db_conf:
        cur.execute('SET search_path TO ' + db_conf['SCHEMA'], ())
    return cur


def to_text_snr(acq, snr_array, sep):
    text = acq.date_time
    for sensor_n in range(1, 33):
        s = 'sensor%s' % sensor_n
        text += sep + str(snr_acquisition[acq.id][s]).replace('.', ',')

    return str(text + '\n')

def to_text_sn(acq, snr_array, sep):
    text = acq.date_time
    for sensor_n in range(1, 33):
        s = 'sensor%s' % sensor_n
        text += sep + str(snr_acquisition[acq.id][s][0]).replace('.', ',')
        text += sep + str(snr_acquisition[acq.id][s][1]).replace('.', ',')

    return str(text + '\n')

SEP = '\t'

# configura conexión de la base de datos
_conn_string = (
    ('host=%(HOST)s dbname=%(NAME)s user=%(USER)s ' +
     'password=%(PASSWORD)s') %
    settings.DATABASE
)

# conecta a la base de datos
conn = psycopg2.connect(
    dsn=_conn_string,
    connection_factory=psycopg2.extras.NamedTupleConnection
)

# clean the file and add the header
with open('data.csv', 'w') as f:
    f.write(
        SEP.join(
            ['dt/hr'] +
            map(lambda n: '%s%s' % (n[1], n[0]), product(range(1, 33), ['s', 'n']))
        ) + '\n'
    )

snr_acquisition = defaultdict(dict)

# consulta adquisición
cursor_acq = db_cursor(conn)

sql = '''
SELECT
  id,
  TO_CHAR(date_time, 'YYYY-MM-DD HH24:MI:SS') as date_time
  FROM acquisition
'''
cursor_acq.execute(sql, ())
count = 0
for acq in cursor_acq:
    # consulta adquisición de señal
    sql = 'select * from acquisition_data_quartz where acquisition=%s'

    cursor_data = db_cursor(conn)
    cursor_data.execute(sql, (acq.id,))

    data = defaultdict(list)

    status_tmp = False

    data_signal = cursor_data.fetchall()

    if len(data_signal) == 0:
        continue

    for line in data_signal:
        status_tmp = True

        for sensor_n in range(1, 33):
            s = 'sensor%s' % sensor_n
            data[s].append(line.__dict__[s])

    # para cada adquisición calcular el SNR
    for sensor_n in range(1, 33):
        s = 'sensor%s' % sensor_n
        snr_acquisition[acq.id][s] = snr(np.array(data[s][50:]))

    cursor_data.close()

    # escribe archivo
    with open('data.csv', 'a') as f:
        f.write(to_text_sn(acq, snr_acquisition, SEP))

    '''
    if status_tmp:
        break  # prueba inicial con la primera adquisición
        pass
    '''
    count += 1
    print(count)

cursor_acq.close()
