from __future__ import division, print_function
import numpy as np


def equal(scalar1, scalar2, tolerance=1e-10):
    """

    @param scalar1:
    @param scalar2:
    @param tolerance:
    @return:
    """
    return abs(scalar1 - scalar2) < tolerance


def printing(vector):
    text = '['
    text += ','.join(['%.55f' % v for v in vector])
    text += ']'
    print(text)


def inner_product(x, y):
    """
    Equal to the dot function: np.dot
    """
    return np.sum([x[i] * y[i] for i in range(x.size)])


def projection(u, v):
    return (np.dot(v, u)/np.dot(u, u)) * u


def test():
    v1 = np.array([3, 1])
    v2 = np.array([2, 2])
    V = [v1, v2]

    u2 = projection(*V)

    np.testing.assert_array_almost_equal(v2 - u2, np.array([-2/5, 6/5]))

    v1 = np.array([0.8660, 0.5000, 0.])
    v2 = np.array([0., 0.5000, 0.8660])
    V = [v1, v2]

    u2 = projection(*V)

    np.testing.assert_array_almost_equal(v2 - u2, np.array([-0.223616, 0.387302, 0.894423]))


if __name__ == '__main__':
    test()
