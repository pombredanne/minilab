from StringIO import StringIO

import psycopg2
import time

settings = {
    'HOST': 'localhost',
    'NAME': 'dbname',
    'USER': 'username',
    'PASSWORD': 'password',
}

_conn_string = (
    ('host=%(HOST)s dbname=%(NAME)s user=%(USER)s ' +
     'password=%(PASSWORD)s') % settings
)

conn = psycopg2.connect(dsn=_conn_string)

cur = conn.cursor()
cur.execute('SET search_path TO mswim')

rows = []
for i in range(15000):
    rows.append(
        '%s\tdev0\tNIDAQmx USB\ 6251, 32 channels\t2009-01-01 00:00:00\t\N\n' % (
            i + 5
        )
    )

f = StringIO(''.join(rows))

t = time.time()
cur.copy_from(
    f, 'device', columns=(
        'id', 'name', 'description',
        'date_operation_beginning', 'date_operation_end')
)
conn.commit()

print('%f' % (time.time() - t))

# 0.181618
# 0.204022
# 0.211497
# 0.227520
# 0.218092
# 0.216576

cur.execute('delete from device where id > 2')
conn.commit()