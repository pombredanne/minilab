# -*- coding: utf-8 -*-
import signal
from scipy import fftpack
from matplotlib import pyplot as plt
import scipy
from numpy import s_
import numpy as np

data_sum = 0
data_avg = 0
samp_cnt = 0

def sampAvg(data_val):
    global data_sum, data_avg, samp_cnt
    samp_cnt += 1
    data_sum += data_val
    data_avg = data_sum / samp_cnt
    return data_avg


def threshold_more_frequent(data):
    """
    Gets the threshold more frequent

    """
    frequency, values = np.histogram(data, 2)
    return values[1]

##_file = '/home/ivan/dev/pydev/lab/grafico/highstock/data/20130401_110658_piezoQuartzo_DadosBrutos.txt'

# señal de ruído
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_162518_piezoQuartzo_DadosBrutos.txt'
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_163036_piezoQuartzo_DadosBrutos.txt'

# m1 fail
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_161755_piezoQuartzo_DadosBrutos.txt'

# m2_fail
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130517_122608_piezoQuartzo_DadosBrutos.txt'
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_161526_piezoQuartzo_DadosBrutos.txt'
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_163150_piezoQuartzo_DadosBrutos.txt'
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_155351_piezoQuartzo_DadosBrutos.txt'

# señal de valor pequeño
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130627_074755_piezoQuartzo_DadosBrutos.txt'

#_file ='/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_163404_piezoQuartzo_DadosBrutos.txt'
#_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_150239_piezoQuartzo_DadosBrutos.txt'



_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/dados-brutos 20130912/20130912_105127_piezoQuartzo_DadosBrutos.txt'


raw = open(_file).read().splitlines()[23:]
# print(raw[:100])
data_raw = map(lambda line: map(lambda v: float(v.replace(',', '.')),
                                line.split()), raw)
#data_raw = data_raw[-1:0:-1]
ndata = np.array(data_raw)
# remove first item (column 0) for axle 1 (column)
ndata = np.delete(ndata, 0, 1)
ndata = np.delete(ndata, s_[1:], 1)

_min  = min(ndata)

_mean = np.mean(ndata)
_std = np.std(ndata)
_snr = (_mean/_std)**2
_snr2 = (_mean/_std)**2

#plt.plot(ndata_raw)
sig = ndata
nsig = np.array(ndata)
for k,v in enumerate(sig):
    nsig[k] = sampAvg(v)

peak = np.zeros(15000)
peak[int(15000*0.95)] = 0.5
sdata = np.sort(ndata, axis=None)

cutoff = threshold_more_frequent(ndata)
data_cutoff = np.array(filter(lambda v: v<=cutoff, ndata))
# np.sqrt((data ** 2).mean())
assert np.square(np.mean(data_cutoff**2)) == np.square((data_cutoff**2).mean())
__rms = np.square((ndata**2).mean())
__delta = __rms * 5
print(len(data_cutoff))
print(cutoff)
print(__rms)
print(__rms*5)
plt.plot(ndata)
plt.plot([__rms] * ndata.size)
plt.plot([__delta] * ndata.size)
plt.show()
exit()
#plt.hist(ndata, 2)
#plt.plot(peak)
#plt.plot(nsig)

print('mean %s' % (np.mean(sdata[:int(sdata.size*0.95)])))
print('std %s' % _std)
print('snr %s' % _snr)

rms = np.sqrt((sig**2).mean())
delta = rms * 5
rms2 = np.sqrt((nsig**2).mean())
print('rms %s' % rms)
print('delta %s' % delta)

#plt.plot([_snr] * sig.size)
#plt.plot([rms] * sig.size)
# plt.plot([_snr*5] * sig.size)
# plt.plot([rms2] * sig.size)

#plt.show()

time_step = 0.0002
period = sig.size
#sig = np.sin(2 * np.pi / period * time_vec) + 0.5 * np.random.randn(time_vec.size)

plt.show()
