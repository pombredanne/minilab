# -*- coding: utf-8 -*-
from scipy import signal
import numpy as np
from numpy import array
from matplotlib.ticker import EngFormatter
from collections import defaultdict
import matplotlib.pyplot as plt
import scipy
import sys

# append location of mswim module
sys.path.append('/home/ivan/dev/pydev/labtrans/mswim/')

from mswim import wim

# read data from file
labwim = wim('/home/ivan/dev/pydev/labtrans/mswim/data/20130401_110658_piezoQuartzo_DadosBrutos.txt')
axles = labwim.axles()
for ax in axles:
    print('Sensor %s: %s axles' % (ax, axles[ax]))