# -*- coding: utf-8 -*-

from scipy import signal
from scipy.fftpack import fft, ifft
from matplotlib import pyplot as plt
import numpy as np
import pylab
from math import pi

threshould = 0.2

def peaks1(_data):
    data = list(_data)
    peaks = []

    while True:
        _max = max(data)
        _max_index = np.where(data==max(data))[0][0]

        if _max <= threshould:
            break

        peaks.append((_max_index, _max))

        #left
        left = _max_index - 1
        while True:
            if data[left] <= threshould:
                break
            left -= 1

        #left
        right = _max_index + 1
        while True:
            if data[right] <= threshould:
                break
            right += 1

        data[left:right] = [0]*abs(right-left)

    return peaks


raw = open('sinal_bruto_filtrado.txt').read().split()
data_raw = map(lambda v: float(v.replace(',', '.')), raw)
#data_raw = data_raw[-1:0:-1]


ndata = np.array(data_raw)
ndata_filt = signal.medfilt(ndata, 7)
npeak = np.zeros(len(ndata))

_peaks1 = peaks1(ndata_filt)

print _peaks1

for i, v in _peaks1:
    npeak[i] = v


plt.plot(ndata)
plt.plot(ndata_filt)
plt.plot(npeak)

plt.show()