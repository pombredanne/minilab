# -*- coding: utf-8 -*-
from __future__ import print_function, division
from itertools import combinations

import sys

sys.path.append('../concepts/')
from vectors.operations import inner_product, printing, equal

import numpy as np


def norm(v):
    """

    @param v:
    @return:
    """
    return np.sqrt(inner_product(v, v))


def is_orthogonal(V):
    """

    @param V:
    @return:
    """
    return all([
        True if equal(np.dot(x, y), 0) else False
        for x, y in combinations(V, 2)
    ])


def is_orthonormal(V):
    """
    Two vectors are orthonormal if:
        - 1. Their dot product is zero.
        - 2.The two vectors are unit vectors.

    @param V:
    @return:
    """
    return all([
        True if is_orthogonal([x, y]) and
        equal(np.dot(x, x), 1) and
        equal(np.dot(y, y), 1) else False
        for x, y in combinations(V, 2)
    ])


def coefficient_expansion(set_vector, x):
    """

    @param set_vector:
    @param x:
    @return:
    """
    # expansion coefficients
    return np.asarray(np.dot(np.matrix(set_vector)**(-1), x))[0]


def test():
    # From the orthogonality restriction, u * v = 0.
    # From the unit length restriction on u, ||u|| = 1.
    # From the unit length restriction on v, ||v|| = 1.

    v1 = np.array([0.6, 0, -0.8])
    v2 = np.array([-0.8, 0, -0.6])
    v3 = np.array([0, 1, 0])

    np.testing.assert_(is_orthonormal(v1, v2, v3))

    # Orthonormal Basis Expansions
    # link -> http://cnx.org/content/m10760/latest/
    # In general, given a basis {b0,b1} and a vector x ∈ ℝ2,
    # how do we find the α0 and α1 such that:
    # x = α0 b0 + α1 b1
    x = np.array([1, 2])
    e = [
        np.array([1, 0]),
        np.array([0, 1]),
    ]

    h = [
        np.array([1, 1]),
        np.array([1, -1]),
    ]

    a0, a1 = 1, 2
    np.testing.assert_array_equal(e[0]*a0 + e[1]*a1, x)
    np.testing.assert_array_equal(
        coefficient_expansion(e, x),
        np.array([a0, a1])
    )

    a0, a1 = 3/2, -1/2
    np.testing.assert_array_equal(h[0]*a0 + h[1]*a1, x)
    np.testing.assert_array_equal(
        coefficient_expansion(h, x),
        np.array([a0, a1])
    )

    print('pass')

if __name__ == '__main__':
    test()