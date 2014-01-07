# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 16:32:32 2013

@author: ivan
"""
import numpy as np

def peaks(data, step):
    data = data.ravel()
    length = len(data)
    if length % step == 0:
        data.shape = (length/step, step)
    else:
        data.resize((length/step, step))
    max_data = np.maximum.reduce(data,1)
    min_data = np.minimum.reduce(data,1)
    
    return np.concatenate((max_data[:,np.NewAxis], min_data[:,np.NewAxis]), 1)

x = np.sin(np.arange(0, 3.14, 1e-5))
peaks(x,1000)