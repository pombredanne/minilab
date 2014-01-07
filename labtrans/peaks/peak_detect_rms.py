# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 15:35:51 2013

@author: marcos

"""
import numpy as np
# from math import pi, log
# from scipy import fft, ifft
# from scipy.optimize import curve_fit


def _threshold(data):
    frequency, values = np.histogram(ndata, 100)
    amount = []
    threshold = 0
    for key, freq in enumerate(frequency):
        amount.append((freq, values[key]))
        if sum(map(lambda v: v[0], amount))/float(ndata.size) >= 0.95:
            threshold = values[key+1]
            break

    return threshold


def _rms2(data, delta=0.98):
    _data = np.sort(data)[:int(len(data)*delta)]

    return np.sqrt(_data**2).mean()


def _datacheck_peakdetect(x_axis, y_axis):
    """
    @return: tuple with numpy x_axis and numpy y_axis

    """
    if x_axis is None:
        x_axis = range(len(y_axis))

    if len(y_axis) != len(x_axis):
        raise (ValueError,
               'Input vectors y_axis and x_axis must have same length')

    return np.array(x_axis), np.array(y_axis)

def peakdetect(y_axis, x_axis=None, lookahead=300, delta=0):
    """
    Converted from/based on a MATLAB script at:
    http://billauer.co.il/peakdet.html

    function for detecting local maximas and minmias in a signal.
    Discovers peaks by searching for values which are surrounded by lower
    or larger values for maximas and minimas respectively

    keyword arguments:
    y_axis -- A list containg the signal over which to find peaks
    x_axis -- (optional) A x-axis whose values correspond to the y_axis list
        and is used in the return to specify the postion of the peaks. If
        omitted an index of the y_axis is used. (default: None)
    lookahead -- (optional) distance to look ahead from a peak candidate to
        determine if it is the actual peak (default: 200)
        '(sample / period) / f' where '4 >= f >= 1.25' might be a good value
    delta -- (optional) this specifies a minimum difference between a peak and
        the following points, before a peak may be considered a peak. Useful
        to hinder the function from picking up false peaks towards to end of
        the signal. To work well delta should be set to delta >= RMSnoise * 5.
        (default: 0)
            delta function causes a 20% decrease in speed, when omitted
            Correctly used it can double the speed of the function

    return -- two lists [max_peaks, min_peaks] containing the positive and
        negative peaks respectively. Each cell of the lists contains a tupple
        of: (position, peak_value)
        to get the average peak value do: np.mean(max_peaks, 0)[1] on the
        results to unpack one of the lists into x, y coordinates do:
        x, y = zip(*tab)

    """
    max_peaks = []
    min_peaks = []
    # Used to pop the first hit which almost always is false
    dump = []

    # check input data
    x_axis, y_axis = _datacheck_peakdetect(x_axis, y_axis)
    # store data length for later use
    length = len(y_axis)

    # perform some checks
    if lookahead < 1:
        raise ValueError, "Lookahead must be '1' or above in value"
    if not (np.isscalar(delta) and delta >= 0):
        raise ValueError, "delta must be a positive number"

    # maxima and minima candidates are temporarily stored in
    # mx and mn respectively
    mn, mx = np.Inf, -np.Inf

    # Only detect peak if there is 'lookahead' amount of points after it

    for index, (x, y) in enumerate(
        zip(x_axis[:-lookahead], y_axis[:-lookahead])
    ):
        if y > mx:
            mx = y
            mxpos = x
        if y < mn:
            mn = y
            mnpos = x

        ####look for max####
        if y < mx-delta and mx != np.Inf:
            # Maxima peak candidate found
            # look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].max() < mx:
                max_peaks.append([mxpos, mx])
                dump.append(True)
                # set algorithm to only find minima now
                mx = np.Inf
                mn = np.Inf
                if index+lookahead >= length:
                    # end is within lookahead no more peaks can be found
                    break
                continue
            # else:  # slows shit down this does
            #    mx = ahead
            #    mxpos = x_axis[np.where(y_axis[index:index+lookahead]==mx)]

        ####look for min####
        if y > mn+delta and mn != -np.Inf:
            # Minima peak candidate found
            # look ahead in signal to ensure that this is a peak and not jitter
            if y_axis[index:index+lookahead].min() > mn:
                min_peaks.append([mnpos, mn])
                dump.append(False)
                # set algorithm to only find maxima now
                mn = -np.Inf
                mx = -np.Inf
                if index+lookahead >= length:
                    # end is within lookahead no more peaks can be found
                    break
            # else:  #slows shit down this does
            #    mn = ahead
            #    mnpos = x_axis[np.where(y_axis[index:index+lookahead]==mn)]

    # Remove the false hit on the first value of the y_axis

    try:
        if dump[0]:
            max_peaks.pop(0)
        else:
            min_peaks.pop(0)
        del dump
    except IndexError:
        # no peaks were found, should the function return empty lists?
        pass

    return [max_peaks, min_peaks]


if __name__ == '__main__':
    import os
    import pylab

    dfile = (
        '/home/%s/dev/pydev/lab/grafico/highstock/data/' +
        '20130401_110658_piezoQuartzo_DadosBrutos.txt'
    ) % os.getenv('USER')

    dfile = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/calibracao/20130627_074755_piezoQuartzo_DadosBrutos.txt'

    raw = open(dfile).read().splitlines()[23:]

    ndata = np.array(
        [x[0] for x in
         map(lambda line:
             map(lambda v: float(v.replace(',', '.')),
                 [line.split()[1]]), raw)]
    )

    samplerate = 5000
    min_peak_dist = 200 # chutei!!
    f = 2 #segun doc 4 >= f >= 1.25
    # deveria ser apenas do noise mas como tem poucos picos
    # considero todo o sinal

    rms = np.sqrt((ndata**2).mean())
    rms2 = np.sqrt((ndata[np.where(ndata <= _threshold(ndata))]**2).mean())
    _delta2 = rms2*5

    print('lookahead %s' % (samplerate / min_peak_dist / f))

    maxp, minp = peakdetect(
        ndata,
        lookahead=samplerate / min_peak_dist / f,
        delta=_delta2
    )
    # ndata = abs(ndata)
    peaksd = np.zeros(len(ndata))
    _median = np.median(ndata)
    _mean = np.mean(ndata)

    # pylab.plot(sorted(ndata))
    # ordered_data = sorted(ndata)
    # print(ordered_data[len(ordered_data)/2-1:len(ordered_data)/2+1])

    # pylab.hist(ndata, 100)
    # pylab.show()
    # exit()

    pylab.plot(ndata)

    print(len(maxp))
    print('total %s, %s' % (len(ndata[np.where(ndata <= _threshold(ndata))]), len(ndata[np.where(ndata <= _threshold(ndata))])/15000.))
    print('rms %s' % rms)
    print('delta %s' % (rms*5))
    print('rms2 %s' % rms2)
    print('rms2 95%% minor signals: %s' % _rms2(ndata))
    print('delta2 95%% minor signals: %s' % (_rms2(ndata)*5))
    print('delta2 %s' % _delta2)
    # print('median %s' % _median)
    # print('mean %s' % _mean)

    for p in maxp:
        peaksd[p[0]]=p[1]

    pylab.plot(peaksd)
    pylab.plot([_delta2]*len(ndata))

    # pylab.plot([rms]*len(ndata))
    # pylab.plot([rms2]*len(ndata))
    # pylab.plot([_median]*len(ndata))
    # pylab.plot([_mean]*len(ndata))

    # pylab.plot([0.02]*len(ndata))
    # margen de 10% del threshold
    # pylab.plot([0.02*1.1]*len(ndata))


    pylab.grid()
    pylab.show()
