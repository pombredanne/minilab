# -*- coding: utf8 -*-
from __future__ import print_function, division
import sys
import numpy as np

sys.path.append('../concepts/')
sys.path.append('../externo/')

from vectors.ortho import (
    norm, is_orthonormal,
    is_orthogonal, coefficient_expansion
)

from vectors.dependence import is_basis
from vectors.gram_schmidt import orthonormalize
from gs_orthonormalization import gs_orthonormalization


def test2():
    # COURSERA HOMEWORK 2
    v0 = np.array([1/2, 1/2, 1/2, 1/2])
    v1 = np.array([1/2, 1/2, -1/2, -1/2])
    v2 = np.array([1/2, -1/2, 1/2, -1/2])

    # 1 - OK
    v3 = np.array([-1/2, 1/2, 1/2, -1/2])

    # 2 - OK
    v3 = np.array([1/2, -1/2, -1/2, 1/2])

    np.testing.assert_(is_orthonormal(v0, v1, v2, v3))


def test3():
    # QUESTION 3
    # In the same setup as in Question 2,
    # (if you found several possibilities for v3 just choose one of them).
    # Let y=[2, 1, 0, −1]T
    # what are the expansion coefficients of y in the basis {v0,v1,v2,v3}
    # you found in the previous question?
    v0 = np.array([1/2, 1/2, 1/2, 1/2])
    v1 = np.array([1/2, 1/2, -1/2, -1/2])
    v2 = np.array([1/2, -1/2, 1/2, -1/2])
    v3 = np.array([-1/2, 1/2, 1/2, -1/2])

    y = np.array([2, 1, 0, -1])
    print(coefficient_expansion([v0, v1, v2, v3], y))


def test4():
    print('\nQUESTION 4\n')
    # QUESTION 4
    # In the same setup as in Question 2 and Question 3,
    # Which of the following sets form a basis of R4?
    # (You may have to tick 0, 1 or many boxes)
    v0 = np.array([1/2, 1/2, 1/2, 1/2])
    v1 = np.array([1/2, 1/2, -1/2, -1/2])
    v2 = np.array([1/2, -1/2, 1/2, -1/2])
    v3 = np.array([-1/2, 1/2, 1/2, -1/2])
    y = np.array([2, 1, 0, -1])

    print('{y, v1, v2, v3}')
    print(is_basis([y, v1, v2, v3], 4, verbose=False))
    print('{y, v0, v1, v2}')
    print(is_basis([y, v0, v1, v2], 4, verbose=False))
    print('{y, v1, v2 - v1, v3}')
    print(is_basis([y, v1, v2 - v1, v3], 4, verbose=False))
    print('{y, v0, v2, v3}')
    print(is_basis([y, v0, v2, v3], 4, verbose=False))


def test5():
    # QUESTION 5
    # Let x and y be vectors in R3.
    # In the lecture, we defined the inner product between two
    # vectors as ⟨x,y⟩=x^T * y. This is the standard way of defining it,
    # and probably the one that you have been using since the high school.
    # But that does not mean that there is only one way of defining it.
    # Let's create a new one! We just need to define it in such a way that
    # the properties of the inner product hold for the new definition.
    # For example, consider:
    # <x, y> = x^T [2  3  1
    #               3  1 -3
    #               1 -3  5] * y
    # The answer is not.
    pass


def test6():
    # QUESTION 6
    # Consider a line on the 2-D plane defined by the cartesian basis,
    # {e1,e2} (e1=[10] and e2=[01]).
    # Let x=[x1x2] be the coordinate of a point on the line :
    # You want to apply the following transformation to the line :
    # A translation of [1, −1]T followed by a scaling of √2 followed by a
    # rotation in the trigonometric (counter-clockwise)
    # direction (with the origin as center) by 3π/4
    # to obtain (the figure is only here to help you visualize the transformation)
    # This transformation maps the point of coordinates x to a point of
    # coordinates y. Since the transformation is affine, one can write it as

    # What are the numerical values of a,b,c,d,f,g ?

    e1 = np.array([1, 0])
    e2 = np.array([0, 1])


def test7():
    print('\nQUESTION 7\n')
    # QUESTION 7
    # This question is related to the proposed Numerical Examples.
    # If you have not done them yet, please do so before answering.
    # The Gram-Schmidt process  takes a linearly independent set
    # V={v1,v2,...vk} and produces an orthonormal set
    # E={e1,e2,...ek}, that spans the same subspace of Rn as V.

    # Consider the three vectors

    v1 = np.array([0.8660, 0.5000, 0])
    v2 = np.array([0, 0.5000, 0.8660])
    v3 = np.array([1.7320, 3.0000, 3.4640])
    V = [v1, v2, v3]

    # Does the output matrix in this case, represent a set of orthonormal vectors?

    # Some concepts:
    # In linear algebra, the rank of a matrix A is a measure of the
    # "nondegenerateness" of the system of linear equations and linear
    # transformation encoded by A. There are many possible definitions of rank,
    # including the size of the largest collection of linearly independent
    # columns of A. Others are listed in the following section. The rank is one of
    # the fundamental pieces of data associated with a matrix.
    # The rank is commonly denoted by either rk(A) or rank(A); sometimes the
    # parentheses are unwritten, as in rk A.
    gram_schmidit_result = [
        [0.866019, 0.500011, 0.],
        [0.223616, 0.387302, 0.894423],
        [0., 0., 0.]
    ]
    assert is_orthogonal(V) is False
    assert is_orthonormal(V) is False

    gram_schmidit_result = orthonormalize(V)
    print(gram_schmidit_result)
    assert is_orthogonal(gram_schmidit_result) is True
    assert is_orthonormal(gram_schmidit_result) is True

    E = gs_orthonormalization(V)
    assert is_orthonormal(E.tolist()) is True
    # It is a set of orthonormal vectors, because rank(E)=3.
    print('rank(E)=3: %s' % np.rank(E))

    # It is not a set of orthonormal vectors, because ETE≠I.
    print('ET E != I: %s' % (E.transpose() * E != E.I))
    # It is not a set of orthonormal vectors, because rank(E)>1.
    # It is a set of orthonormal vectors, because det(E)>0. (WRONG)
    # It is a set of orthonormal vectors, because det(E)=0.
    print('det(E)=0 : %s' % np.linalg.det(E))
    # It is a set of orthonormal vectors, because ETE=I.


def test():
    test7()

if __name__ == '__main__':
    test()