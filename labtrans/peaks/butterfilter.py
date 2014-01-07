# -*- coding: utf-8 -*-
from math import pi
from numpy import arange, sin
from scipy.signal import butter, lfilter, filtfilt
import matplotlib.pyplot as plt


freq = 100
t = arange(0,1,.01);
w = 2*pi*1 # 1 Hz
y = sin(w*t)+0.1*sin(10*w*t)
# Butterworth filter
b, a = butter(4, (5/(freq/2)), btype = 'low')
y2 = lfilter(b, a, y)  # standard filter
y3 = filtfilt(b, a, y) # filter with phase shift correction
# plot

ax1 = plt.subplot(111)
ax1.plot(t, y, 'r', linewidth=2, label = 'raw data')
ax1.plot(t, y2, 'b', linewidth=2, label = 'filter @ 5 Hz')
ax1.plot(t, y3, 'g', linewidth=2, label = 'filtfilt @ 5 Hz')
ax1.legend(frameon=False, fontsize=14);
ax1.set_xlabel("Time [s]"); ax1.set_ylabel("Amplitude");
plt.show()