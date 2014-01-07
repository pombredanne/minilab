# -*- coding: utf8 -*-
from __future__ import division, print_function
from matplotlib import pyplot

import numpy as np
import sys

sys.path.append('../concepts')

from eulers_formula import e


def f(k, N):
    """
    w_n(k) = e^(j ((2*pi)/N) * k)

    @param k:
    @param N:
    @return:
    """
    return np.array([e(((2*np.pi)/N)*k*n) for n in range(N)])


def sig_real(sig):
    return [s.real for s in sig]


def sig_imaginary(sig):
    return [s.imag for s in sig]


def test():
    N = 64

    for n in range(N):
        sig = f(n, N)

        pyplot.subplot(211)
        pyplot.grid()
        pyplot.axis([-2, 66, -2, 2])
        pyplot.stem(sig_real(sig))
        pyplot.subplot(212)
        pyplot.grid()
        pyplot.axis([-2, 66, -2, 2])
        pyplot.stem(sig_imaginary(sig))
        pyplot.show()


if __name__ == '__main__':
    test()