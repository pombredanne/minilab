# -*- coding: utf-8 -*-
"""
Temperature Scan

"""
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from datetime import datetime

import settings
from conn import db_connect, db_cursor

temp5 = 0
temp17 = 0

with open('c:/tmp/temp5') as f:
    temp5 = float(f.read())

with open('c:/tmp/temp17') as f:
    temp17 = float(f.read())

conn = db_connect(settings)
cur = db_cursor(conn, settings)

cur.execute(
'''
INSERT INTO temperature (date_time, temp5, temp17)
VALUES (DEFAULT, %s, %s)
''', (temp5, temp17))

conn.commit()

cur.close()
conn.close()

print('Temperature read.')