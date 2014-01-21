from __future__ import division, print_function
import numpy as np
from numpy import testing
from university.coursera.dsp.concepts.vectors.operations import inner_product


def norm(x):
    """
    The inner product of x with itself is always non-negative.
    This product allows us to define the "length"
    of a vector x through square root:

    To test it on wolframalpha do:
        - Norm[{v0, v1, v2}]

    """
    return np.sqrt(np.dot(x, x))


def distance(x, y):
    """
    This distance function is called the Euclidean metric.
    This formula expresses a special case of the Pythagorean theorem.
    This distance function (which makes a metric space) is sufficient to
    define all Euclidean geometry, including the dot product.
    Its vectors form an inner product space (in fact a Hilbert space),
    and a normed vector space.

    The metric space structure is the main reason behind the use of real
    numbers R, not some other ordered field, as the mathematical foundation of
    Euclidean (and many other) spaces. Euclidean space is a
    complete metric space, a property which is impossible to achieve
    operating over rational numbers, for example.

    """
    return np.sqrt(np.sum([(x[i] - y[i])**2 for i in range(x.size)]))


def test():
    approx = testing.assert_approx_equal
    x = np.array([1, 2, 3])
    approx(norm(x), 3.74166, 5)
    approx(np.dot(x, x), inner_product(x, x))

    x = np.array([10, 20, 30])
    approx(norm(x), 37.4166, 5)

    x = np.array([10, 20])
    approx(norm(x), 22.3607, 5)

    x = np.array([10, 20, 70, 10])
    approx(norm(x), 74.162, 5)

    x = np.array([10, 20, 70, 10, 99, 44])
    approx(norm(x), 131.29, 5)

    x = np.array([1, 2, 3])
    y = np.array([1, 7, 10])
    approx(distance(x, y), 8.60233, 5)

    x = np.array([1, 2, 3, 10])
    y = np.array([1, 7, 10, 70])
    approx(distance(x, y), 60.6135, 5)

    print('pass')

if __name__ == '__main__':
    test()