from __future__ import print_function

import psycopg2

dns = 'host=localhost dbname=? user=? password=?'
conn = psycopg2.connect(dns)
cur = conn.cursor()

cur.execute('DELETE FROM train ')

with open('train.csv', 'r') as f:
    data = f.read().splitlines()
    header = False
    for row in data:
        data_row = row.split('\t')
        if not header:
            header = True
            continue
        sql = 'INSERT INTO train VALUES(%s' + (',%s'*11) + ');'

        data_row[0] = int(data_row[0])
        data_row[1] = int(data_row[1])
        data_row[2] = int(data_row[2])
        data_row[3] = str(data_row[3])
        data_row[4] = str(data_row[4])
        data_row[5] = float(data_row[5] if data_row[5] != '' else 0)
        data_row[6] = int(data_row[6])
        data_row[7] = int(data_row[7])
        data_row[8] = str(data_row[8])
        data_row[9] = float(data_row[9])
        data_row[10] = str(data_row[10])
        data_row[11] = str(data_row[11])

        cur.execute(sql, tuple(data_row))
        conn.commit()