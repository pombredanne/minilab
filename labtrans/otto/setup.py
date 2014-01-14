# -*- coding: utf-8 -*-
"""

"""
from __future__ import division, print_function, unicode_literals
from conn import db_connect, db_cursor
from copy import deepcopy
import settings

db_name = settings.DATABASE['NAME']
settings.DATABASE['NAME'] = 'postgres'

# conecta a la base de datos
conn = db_connect(settings, as_command=True)
cur = db_cursor(conn, settings)
try:
    cur.execute('CREATE DATABASE lab_temperature')
except:
    pass
cur.close()
conn.close()

settings.DATABASE['NAME'] = db_name

# conecta a la base de datos
conn = db_connect(settings)
cur = conn.cursor()

sql = '''
CREATE TABLE temperature (
  date_time TIMESTAMP NOT NULL DEFAULT NOW()::timestamp,
  temp5 FLOAT,
  temp17 FLOAT
)
'''

try:
    cur.execute(sql)
except:
    pass
conn.commit()
cur.close()
conn.close()
print('Setup finished.')
