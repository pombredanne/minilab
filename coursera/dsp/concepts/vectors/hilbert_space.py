from __future__ import division
import numpy as np
from coursera.dsp.concepts.vectors.euclidean_space import inner_product


def norm(x):
    """
    The inner product of x with itself is always non-negative.
    This product allows us to define the "length"
    of a vector x through square root:

    To test it on wolframalpha do:
        - Norm[{v0, v1, v2}]

    """
    return np.sqrt(np.dot(x, x))


def test():
    """

    """

    '''
    one of the most familiar examples of a hilbert space is the euclidean
    space consisting of three-dimensional vectors, denoted by R3,
    and equipped with the dot product. the dot product takes two vectors
    x and y, and produces a real number x*y. if x and y are represented in
    cartesian coordinates, then the dot product is defined by
    '''

    # It is symmetric in x and y: x * y = y * x
    x = np.array([1, 2, 3])
    y = np.array([4, 5, 30])
    assert inner_product(x, y) == inner_product(y, x)

    # It is linear in its first argument:
    # (ax1 + bx2) * y = ax1 * y + bx2 * y
    # for any scalars a, b, and vectors x1, x2, and y.
    x1 = np.array([1, 2, 3])
    x2 = np.array([4, 5, 30])
    y = np.array([42, 50, 75])
    a = 5
    b = 13
    assert inner_product((a*x1 + b*x2), y) == \
        inner_product(a*x1, y) + inner_product(b*x2, y)

    # Hilbert-space

    # Conjugate symmetry:
    # <x, y> = <y, x>*
    x = np.array([1+1j, 2+ 7j, 3+2j]).astype(complex)
    y = np.array([4+3j, 5+1j, 30+10j]).astype(complex)
    #assert np.dot(x, y) == np.dot(x.conjugate(), y.conjugate())
    print(np.dot(x, y))
    print(np.dot(x.conjugate(), y.conjugate()))

    # complex number
    z = np.array([1+1j, 2+ 7j, 3+2j])
    w = np.array([4+3j, 5+1j, 30+10j])
    a = 10+5j
    b = 15+3j

    # The inner product
    # this calculus doesn't work
    #np.testing.assert_equal(
    #    np.dot(z, w), np.dot(w.conjugate(), z.conjugate())
    #)

    # The inner product is linear in its first argument.
    # For all complex numbers a and b
    x1 = np.array([4+7j, 6+9j, 40+20j])
    x2 = np.array([5+2j, 10+3j, 45+30j])
    y = z
    np.testing.assert_equal(
        np.dot(a*x1 + b*x2, y),
        a*np.dot(x1, y) + b*np.dot(x2, y)
    )

    # The inner product of an element with itself is positive definite
    assert np.dot(x1, x1) >= 0

    # It follows from properties 1 and 2 that a complex inner product is
    # antilinear in its second argument, meaning that
    y1 = x1
    y2 = x2
    x = z

    e1 = np.dot(x, a*y1 + b*y2)
    e2 = a.conjugate() * np.dot(x, y1) + b.conjugate() * np.dot(x, y2)

    # np.assert_equal(e1, e2)


    print('pass')

if __name__ == '__main__':
    test()