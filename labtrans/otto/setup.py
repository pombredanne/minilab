# -*- coding: utf-8 -*-
"""

"""
from __future__ import division, print_function, unicode_literals
from conn import db_connect, db_cursor

settings_template = '''# -*- coding: utf-8 -*-
"""
Local Settings file

"""
DEBUG = True

_PATH_ROOT = __file__[:-len(__name__) + 2]

DEFAULT_FROM_EMAIL = 'ivan.ogassawara@labtrans.ufsc.br'

DATABASE = {
        'ENGINE':   'postgresql',
        'NAME':     'lab_temperature',
        'USER':     '***',
        'PASSWORD': '***',
        'HOST':     '***',
        'PORT':     '5432'
}

email = {
    'to': 'ivan.ogassawara@gmail.com',
    'from': 'ivan.ogassawara@labtrans.ufsc.br',
    'smtp-server': 'smtp.labtrans.ufsc.br'
}
'''

try:
    import settings
except:
    with open('settings.py', 'w') as f:
        f.write(settings_template)
        print('Configure o arquivo settings.py e tente executar novamente.')
        exit()

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
