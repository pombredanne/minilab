from __future__ import print_function

import numpy as np
from matplotlib import pylab

def local_maxima(data):
    """
    Detection/Intensity threshold

    Return a list with peaks tuple informations (index, value).
    This algorithm considers the peak is the max value between on
    threshold limits.

    """
    data = data.copy()
    peaks = []

    threshold = 0.1
    threshold_noise = threshold * 1.8
    clean_signal = min(data)

    data = np.where(data > threshold_noise, data, clean_signal)

    while True:
        _max = max(data)
        _max_index = np.where(data == max(data))[0][0]

        # considers 10% of noise
        if _max <= threshold_noise:
            break

        peaks.append((_max_index, _max))

        # left
        left = _max_index - 1
        while True:
            if left < 0:
                left = 0

            if left <= 0 or data[left] <= threshold:
                break
            left -= 1

        # right
        right = _max_index + 1
        while True:
            if right > data.size:
                right = data.size - 1

            if right >= data.size or data[right] <= threshold:
                break
            right += 1
        # log.append('left: %s' % left)
        # log.append('right: %s' % right)
        data[left:right] = [clean_signal] * abs(right - left)


    return sorted(peaks, key=lambda peak: peak[0])


def snr(acquisition):
    """
    Retorna una lista con el SNR de cada sensor

    """

    def min_peak(_peaks):
        if not _peaks:
            return [0, 0]
        return min(_peaks, key=lambda v: v[1])

    peaks = local_maxima(acquisition)

    limit_min = 0
    limit_max = acquisition.size

    noisy_data = []

    # plot
    # data_cut = np.zeros(acquisition.size)

    for p in peaks:
        calc_min = p[0] - 200
        calc_max = p[0] + 200
        pmin = calc_min if calc_min > limit_min else limit_min
        pmax = calc_max if calc_max < limit_max else limit_max

        # plot
        # data_cut[pmin] = 3
        # data_cut[pmax - 1] = 3

        if p[0] > limit_min:
            noisy_data += list(acquisition[limit_min:pmin-1])

        limit_min = pmax

    if limit_min < limit_max:
        noisy_data += list(acquisition[limit_min:limit_max])

    noisy_data = np.array(noisy_data)

    # noisy amplitude
    n = max(noisy_data) - min(noisy_data)

    # signal amplitude
    s = min_peak(peaks)[1] - max(noisy_data)

    # plot
    '''
    data_cut[min_peak(peaks)[0]] = min_peak(peaks)[1]
    noisy_cut_max = np.array([max(noisy_data)] * noisy_data.size)
    noisy_cut_min = np.array([min(noisy_data)] * noisy_data.size)
    pylab.figure(figsize=(6*3.13, 4*3.13))
    pylab.plot(acquisition)
    pylab.plot(data_cut)
    pylab.plot(noisy_cut_max)
    pylab.plot(noisy_cut_min)
    pylab.show()
    print(peaks)
    '''

    # SNR
    return s, n
