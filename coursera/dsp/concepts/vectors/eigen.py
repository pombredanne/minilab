# -*- coding: utf8 -*-
"""
An eigenvector of a square matrix A is a non-zero vector v that, when the
matrix is multiplied by v, yields a constant multiple of v,
the multiplier being commonly denoted by \lambda. That is:

A v = \lambda v

(Because this equation uses post-multiplication by v,
it describes a right eigenvector.)

The number \lambda is called the eigenvalue of A corresponding to v.[1]

"""
from __future__ import division, print_function
from numpy import linalg
import numpy as np
import sys

sys.path.append('../')

from vectors.ortho import coefficient_expansion


def eigen_value(v, r, exception=False):
    f = None

    if v[0][0] > r[0][0]:
        f = lambda nv, nr: nv / nr
    else:
        f = lambda nv, nr: nv * nr

    s = f(v[0][0], r[0][0])

    if exception:
        try:
            assert f(v[1][0], r[0][1]) == s

        except Exception as e:
            raise(e)
        return

    assert f(v[1][0], r[0][1]) == s
    return s


def test():
    A = np.matrix([[3, 1], [1, 3]])
    v = np.matrix([4, -4])
    Av = A*v.T
    assert eigen_value(np.asarray(Av), np.asarray(v)) == 2

    v = np.matrix([0.000001, 1])
    Av = A*v.T
    err = False

    try:
        eigen_value(np.asarray(Av), np.asarray(v), True)
    except:
        err = True

    assert err





if __name__ == '__main__':
    test()