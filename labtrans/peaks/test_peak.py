# -*- coding: utf-8 -*-
# requirements sudo pip install networkx
import numpy as np
import matplotlib.pyplot as plt

import nitime.utils as utils
# import nitime.timeseries as ts
# import nitime.viz as viz

ar_seq, nz, alpha = utils.ar_generator(N=128, drop_transients=10)
ar_seq -= ar_seq.mean()

n_trials = 12

fig_snr = []
sample = []
fig_tseries = []

for idx, noise in enumerate([1, 10, 50, 100]):
    sample.append(np.ones((n_trials, ar_seq.shape[-1])) + ar_seq)
    n_points = sample[-1].shape[-1]

for trial in  xrange(n_trials):
    sample[-1][trial] += np.random.randn(sample[-1][trial].shape[0]) * noise

sample_mean = np.mean(sample[-1], 0)

fig_tseries.append(plt.figure())
ax = fig_tseries[-1].add_subplot(1, 1, 1)
ax.plot(sample[-1].T)
ax.plot(ar_seq, 'b', linewidth=4)
ax.plot(sample_mean, 'r', linewidth=4)
ax.set_xlabel('Time')
ax.set_ylabel('Amplitude')
plt.show()