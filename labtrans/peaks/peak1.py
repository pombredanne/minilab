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
"""
raw = open('sinal_bruto_filtrado.txt').read().split()
data_raw = np.array(map(lambda v: float(v.replace(',', '.')), raw))
data_peak = [0] * len(data_raw)
"""
from scipy import s_

_file = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130626_153402_piezoQuartzo_DadosBrutos.txt'
raw = open(_file).read().splitlines()[23:]

ndata = np.array([
    x[0] for x in map(lambda line:
                      map(lambda v: float(v.replace(',', '.')),
                          [line.split()[1]]), raw)
])

_mean = np.mean(ndata)
_std = np.std(ndata)
_snr = (_mean/_std)**2

print 'mean: ', _mean
print 'standard deviation: ', _std
print 'snr: ', _snr

data_peak = [0] * len(ndata)

print(len(ndata))

widths = np.arange(90 ,100)
cwtmat = signal.cwt(ndata,signal.ricker,widths)

peakind = signal.find_peaks_cwt(
    ndata,
    widths,
    min_snr=_mean*100,
    noise_perc=_snr
)

print(len(peakind)) #, data_raw[peakind]

for ip in peakind:
    data_peak[ip] = ndata[ip]

plt.plot(ndata)
plt.plot(data_peak)

plt.show()