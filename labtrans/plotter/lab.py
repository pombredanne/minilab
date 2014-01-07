# -*- coding:utf-8 -*-
import sys

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import EngFormatter

local_path = '/'.join(sys.path[0].split('/')[:-2]) + '/'
sys.path.insert(0, local_path + 'mswim/')

from mswim import WimSys
a = ''
x = True if a else False
print(x)
exit()
root_file = '/home/ivan/dev/pydev/datos/mswim/calibracao/'
    
labwim = WimSys('host=150.162.176.222 dbname=labdb user=lab password=lab')

#labwim.save_file(root_file + '20130626_150243_piezoQuartzo_DadosBrutos.txt')
wimdata = labwim.search_acquisition(1)
wimdata.extract_data_array()
print(wimdata.axles())

labwim.plot(wimdata)

"""
from datetime import datetime, timedelta

acq_date, acq_time = ('2013/06/26', '11:45:14,9430323499424465829')
acq_time = acq_time.split(',')
acq_time = ','.join((acq_time[0], acq_time[1][:6]))
date_object = datetime.strptime('%s %s' % (acq_date, acq_time), '%Y/%m/%d %H:%M:%S,%f')

#0,000200
delta_time = float('0,000200'.replace(',', '.'))
delta_time = timedelta(seconds=delta_time)
new_time = date_object + delta_time
print(new_time)
"""

"""
import datetime
s = "2010-01-01 18:48:14,631829"
print(datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S,%f"))
"""

import os

root_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/'

_files = [f for f in os.listdir(root_file) if f.endswith('_piezoQuartzo_DadosBrutos.txt')]
print _files