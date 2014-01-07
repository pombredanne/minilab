from __future__ import division
import numpy as np
import cmath


def equal_complex(*arrays):
    size = arrays[0].size

    def printing(i, a, b):
        print i,
        print ' --->',
        print np.real(a[i]), np.real(b[i])
        print np.imag(a[i]), np.imag(b[i])
        print 'real -> ',
        print '%s' % np.real(a[i]) == '%s' % np.real(b[i]),
        print 'imag -> ',
        print np.imag(a[i]) == np.imag(b[i])
        return True
    print size
    print arrays[0:-1]
    print arrays[1:]
    return np.alltrue([
        printing(i, a, b) and np.real(a[i]) == np.real(b[i]) and
        np.imag(a[i]) == np.imag(b[i])
        for i in range(size)
        for a in arrays[0:-1]
        for b in arrays[1:]
    ])


def test():
    z = np.array([1+1j, 2+ 7j, 3+2j])
    w = np.array([4+3j, 5+1j, 30+10j])
    a = 10+5j
    b = 15+3j

    # (z + w)* = z* + w*
    np.testing.assert_array_equal(
        (z+w).conjugate(), (z.conjugate() + w.conjugate())
    )

    # (z * w)* = z* * w*
    np.testing.assert_array_equal(
        (z*w).conjugate(), (z.conjugate() * w.conjugate())
    )

    # z* = z when z is real
    z = np.array([1, 2, 3]).astype(complex)
    np.testing.assert_array_equal(
        z.conjugate(), z
    )

    # (z**n)* = (z*)**n for any integer n
    z = np.array([1+1j, 2+ 7j, 3+2j])
    n = 5
    np.testing.assert_array_equal(
        (z**n).conjugate(), (z.conjugate())**n
    )

    # |z*| = |z|
    np.testing.assert_array_equal(
        np.abs(z.conjugate()), np.abs(z)
    )

    # |z|**2 = z * z* = z* * z
    e1 = (np.absolute(z).astype(complex) * np.absolute(z).astype(complex))
    e2 = z * z.conjugate()
    e3 = z.conjugate() * z

    np.testing.assert_array_almost_equal(e1, e2)
    np.testing.assert_array_almost_equal(e3, e2)

    # (z*)* = z (involution, the conjugate of the conjugate of a complex num.)
    np.testing.assert_array_almost_equal(
        z.conjugate().conjugate(), z
    )

    # z**(-1) = (z*) / (z**2) if z is non-zero
    # this calculus doesn't work
    #np.testing.assert_array_almost_equal(
    #    z**(-1), (z.conjugate()) / (z**2)
    #)

    print('pass')


if __name__ == '__main__':
    test()