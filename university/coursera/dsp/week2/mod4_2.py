# -*- coding: utf8 -*-
"""
### The Fourier Basis ###

in signal notation: w_k[n] = e^(j (2*pi/N) nk)
n vector notation: {w^(k)} with w_n^(k) = e^(j (2*pi/N) nk)


### The Fourier Basis for \C^N

- N orthogonal vectors -> basis for C^N
- vector are not orthonormal. Normalization factor would be 1/sqrt(N)
- will keep normalization factor explicit in DFT formulas


### Basis expansion ###
Analysis formula:
 X_k = <w^(k), x>

Synthesis formula:
 x = (1/N) * (sum (X_k w^(k) for k from 0 to N-1))

 note: 1/N is the factor of normalization


### Change of basis in matrix form ###
  W_N = e^(-j (2*pi/N))

Analysis formula:
 X = W*x

Synthesis formula:
 x = (1/N) * W^H X

 note: H is the permission operator, that is a combination of  transposition
 and conjugation of each element of matrix


### Basis expansion (signal notation) ###

Analysis formula:
X[k] = sum(x[n] e^(-j (2*pi/N)*n*k)
           for n from 0 to N-1
           for k from 0 to N-1)

N-point signal in the frequency domain


Synthesis formula:
x[n] = (1/N) * sum(X[k] * e^(j (2*pi/N)*n*k)
                   for k from 0 to N-1
                   for n from 0 to N-1)

N-point signal in the time domain


### DFT is obviously linear ###
DFT {alpha*x[n]} + beta*y[n]} = alpha*DFT{x[n]} + beta*DFT{y[n]}

- DFT of x[n] = delta[n]

X[k] = sum(delta[n]*e^(-j (2*pi/N)*n*k)
           for n from 0 to N-1)
     = 1

- DFT of x[n] = 1

X[k] = sum(e^(-j (2*pi/N)*n*k)
           for n from 0 to N-1)
     = N*delta[k]

### DFT of x[n] = 3*cos((2*pi/16)*n), x[n] \E \C^64 ###

**note:
cos w = (e^(j w) + e^(-j w)) / 2

x[n] = 3*cos((2*pi/16)*n)
     = 3*cos((2*pi/64)*4*n)
     = (3/2) * [e^(j ((2*pi/64)*4*n)) +
                e^(-j ((2*pi/64)*4*n))]
     = (3/2) * (w_4[n] + w_60[n])

X[k] = <w_x[n], x[n]>
     = <w_k[n], (3/2)*(w_4[n] + w_60(n))>
     = (3/2)*<w_k[n], w_4[n]> + (3/2)*<w_k[n], w_60[n]>

     = \{ 96 for k = 4, 60 else 0

plot:
  p_real = ([0]*64)
  p_real[4] = 100
  p_real[60] = 100

  p_imag = ([0]*64)
"""
from __future__ import division, print_function
from matplotlib import pyplot
import numpy as np


def test1():
    '''
    DFT of x[n] = 3*cos((2*pi/16)*n), x[n] \E \C^64

    **note:
    cos w = (e^(j w) + e^(-j w)) / 2

    x[n] = 3*cos((2*pi/16)*n)
         = 3*cos((2*pi/64)*4*n)
         = (3/2) * [e^(j ((2*pi/64)*4*n)) +
                    e^(-j ((2*pi/64)*4*n))]
         = (3/2) * (w_4[n] + w_60[n])


    X[k] = <w_k[n], x[n]>
         = <w_k[n], (3/2)*(w_4[n] + w_60(n))>
         = (3/2)*<w_k[n], w_4[n]> + (3/2)*<w_k[n], w_60[n]>

         = \{ 96 for k = 4, 60 else 0

    plot:
      p_real = ([0]*64)
      p_real[4] = 100
      p_real[60] = 100

      p_imag = ([0]*64)
    '''
    N = 64
    t = range(N)

    omega = (2*np.pi)/N

    # define w
    w = {}
    for k in t:
        w[k] = [
            np.e**(complex(0, omega*n*k))
            for n in t
        ]

    x = [(3/2) * (
         np.e**(complex(0, +(omega*4*n))) +
         np.e**(complex(0, -(omega*60*n))))
         for n in t]

    X = {}
    for k in t:
        X[k] = sum([
            (3/2)*np.dot(w[k][n], w[4][n]) +
            (3/2)*np.dot(w[k][n], w[60][n])
            for n in t
        ])

    x_real = [_x.real for _x in X]
    x_imag = [_x.imag for _x in X]

    pyplot.grid()

    pyplot.subplot(211)
    pyplot.stem(t, x_real)

    pyplot.subplot(212)
    pyplot.stem(t, x_imag)

    pyplot.show()


def test():
    """

    @return:
    """

    test1()
    pass

if __name__ == '__main__':
    test()