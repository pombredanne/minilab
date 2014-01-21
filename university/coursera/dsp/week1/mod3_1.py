# -*- coding: utf-8 -*-
from __future__ import division
import numpy as np
from matplotlib import pyplot as pylab

xb = np.linspace(-1, 1, 1000)

x1 = np.sin(2*np.pi*xb)
x2 = np.sin(5*np.pi*xb)

xt = x1*x2

t = np.linspace(-1, 1, 1000)

def x(n):
    return np.sin(np.pi*n*t)/float(n)

def sum_k(N):
    vec = [x(2*k+1) for k in range(N+1)]
    '''
    for v in vec:
        pylab.plot(v)
    '''
    #print np.dot(vec[0], vec[1])
    #print np.dot(vec[1], vec[2])
    #print np.dot(vec[0], vec[2])

    # pylab.show()
    return np.sum(vec, axis=0)


pylab.plot(sum_k(100))

pylab.show()
