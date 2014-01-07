# -*- coding: utf-8 -*-
from scipy import signal
from matplotlib import pyplot as plt
import numpy as np
from itertools import permutations
"""
scipy.signal.find_peaks_cwt(
    vector, widths, wavelet=None, 
    max_distances=None, gap_thresh=None, 
    min_length=None, min_snr=1, 
    noise_perc=10
)[source]

vector : ndarray
         1-D array in which to find the peaks.
widths : sequence
         1-D array of widths to use for calculating the CWT matrix. In general, 
         this range should cover the expected width of peaks of interest.
wavelet : callable, optional
          Should take a single variable and return a 1-D array to convolve with
          vector. Should be normalized to unit area. Default is the ricker wavelet.
max_distances : ndarray, optional
                At each row, a ridge line is only connected if the relative max
                at row[n] is within max_distances[n] from the relative max at 
                row[n+1]. Default value is widths/4.
gap_thresh : float, optional
             If a relative maximum is not found within max_distances, 
             there will be a gap. A ridge line is discontinued if there 
             are more than gap_thresh points without connecting a new 
             relative maximum. Default is 2.
min_length : int, optional
             Minimum length a ridge line needs to be acceptable. Default is 
             cwt.shape[0] / 4, ie 1/4-th the number of widths.
min_snr : float, optional
          Minimum SNR ratio. Default 1. The signal is the value of the cwt 
          matrix at the shortest length scale (cwt[0, loc]), the noise is the 
          noise_perc`th percentile of datapoints contained within a window of 
          `window_size around cwt[0, loc].
noise_perc : float, optional
             When calculating the noise floor, percentile of data points 
             examined below which to consider noise. 
             Calculated using stats.scoreatpercentile. Default is 10.


"""

raw = open('sinal_bruto_filtrado.txt').read().split()
data_raw = map(lambda v: float(v.replace(',', '.')), raw)
#data_raw = data_raw[-1:0:-1]
data_raw = np.array(data_raw)
data_peak = [0] * len(data_raw)


"""
xs = np.arange(0, 2*np.pi, 0.05)
data = np.sin(xs)
data_peak = [0] * len(xs)
peakind = signal.find_peaks_cwt(data, np.arange(63,64))
print peakind, xs[peakind], data[peakind]

for ip in peakind:
    data_peak[ip] = data[ip]

plt.plot(xs)
plt.plot(data)
plt.plot(data_peak)

plt.show()

exit()
"""

peakind = signal.find_peaks_cwt(
    data_raw, 
    np.arange(70,80),
    max_distances=None,
    min_snr=2., 
    noise_perc=7.
)


print peakind #, data_raw[peakind]

for ip in peakind:
    data_peak[ip] = data_raw[ip]

plt.plot(data_raw)
plt.plot(data_peak)

plt.show()