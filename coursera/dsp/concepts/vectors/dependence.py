# -*- coding: utf-8 -*-
from __future__ import division, print_function
from operations import equal
import numpy as np

# constants
R3 = 3


def is_linearly_dependent(V):
    """
    An alternative method uses the fact that n vectors in \mathbb{R}^n are
    linearly dependent if and only if the determinant of the matrix
    formed by taking the vectors as its columns is zero.

    @param V:
    @return: bool

    """
    return equal(np.linalg.det(np.matrix(V)), 0.0)


def is_basis(V, R, verbose=False):
    if not len(V) == R:
        if verbose:
            print('No have %s elements.' % R)
        return False

    if not all([v.size == R for v in V]):
        if verbose:
            print('Not in R.')
        return False

    if sum([np.sum(v) for v in V]) == 0:
        if verbose:
            print('Sum equal to 0.')
        return False

    if is_linearly_dependent(V):
        if verbose:
            print('Is linearly dependent.')
        return False

    return True


def test():
    v0 = np.array([2, -3, 1])
    v1 = np.array([4, 1, 1])
    v2 = np.array([0, -7, 1])
    print(is_basis([v0, v1, v2], R3, verbose=True))

    v0 = np.array([1, 6, 4])
    v1 = np.array([2, 4, -1])
    v2 = np.array([-1, 2, 5])
    print(is_basis([v0, v1, v2], R3, verbose=True))

if __name__ == '__main__':
    test()