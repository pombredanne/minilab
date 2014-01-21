# -*- coding: utf8 -*-
from __future__ import division, print_function
import numpy as np


def e(x):
    # Euler's formula
    # e**(ix) = cos(x) + sin(x)j
    return complex(np.cos(x), np.sin(x))


def test():
    for y in range(100):
        x = y * np.pi
        assert (
            np.exp(complex(0, x)) == np.e**(complex(0, x)) ==
            complex(np.cos(x), np.sin(x)) == e(x)
        )

if __name__ == '__main__':
    test()