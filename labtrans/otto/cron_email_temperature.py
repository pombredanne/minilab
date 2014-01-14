# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
from datetime import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

import smtplib
import settings
from conn import db_connect, db_cursor

month = datetime.now().month
year = datetime.now().year

month, year = (month - 1, year) if month > 1 else (12, year - 1)

# prepare template code
with open('template.html') as f:
    template = f.read()

month_ext = {
    1: 'Janeiro',
    2: 'Fevereiro',
    3: 'Março',
    4: 'Abril',
    5: 'Maio',
    6: 'Junho',
    7: 'Julho',
    8: 'Agosto',
    9: 'Setembro',
    10: 'Outubro',
    11: 'Novembro',
    12: 'Dezembro',
}

conn = db_connect(settings)
cur = db_cursor(conn, settings)

cur.execute('''
SELECT
  TO_CHAR(date_time, 'DD/MM/YYYY HH24:MI:SS') AS date_time,
  temp5, temp17
FROM temperature
WHERE
  EXTRACT(YEAR FROM date_time) = %s
  AND EXTRACT(MONTH FROM date_time) = %s
ORDER BY date_time
''' % (year, month))

data = ''

# date_time, temp5, temp17
for line in cur:
    data += '%s;%s;%s\n' % (line.date_time, line.temp5, line.temp17)

data = '''Informe Mensal de Temperatura;

Data e Hora; Temperatura a 5cm; Temperatura a 17cm;
''' + data

cur.close()
conn.close()

email_body = template.replace(
    '{{ mes }}', month_ext[month]
).replace('{{ ano }}', str(year))

# PREPARE THE EMAIL
outer = MIMEMultipart()
outer['Subject'] = 'Informe de Temperatura Mensal'
outer['From'] = settings.email['from']
outer['To'] = settings.email['to']

msg = MIMEText(email_body, 'html')

outer.attach(msg)

msg = MIMEBase('application', 'octet-stream')
msg.set_payload(data)
encoders.encode_base64(msg)
msg.add_header(
    'Content-Disposition', 'attachment',
    filename=('temperature-%s-%s.csv' % (year, month))
)

outer.attach(msg)

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP(settings.email['smtp-server'])
s.sendmail(settings.email['from'], settings.email['to'], outer.as_string())
s.quit()
