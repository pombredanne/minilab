from __future__ import print_function, division

import numpy as np

from operations import projection, printing
from university.coursera.dsp.concepts.vectors.euclidean_space import norm


def orthonormalize(V):
    """

    @param V:
    @return:
    """
    # j = 1
    # return [vk - np.sum([projection(V[i], vk) for i in range(j, k)]) for k, vk in enumerate(V)]
    S = {}
    for i in range(0, len(V[0])):
        S[i] = V[i]/norm(V[i])

        for j in range(1, i-1):
            S[j] = V[j] - projection(S[i], V[j])

    return [S[i] for i in list(S)]


def test():
    v1 = np.array([0.8660, 0.5000, 0])
    v2 = np.array([0, 0.5000, 0.8660])
    v3 = np.array([1.7320, 3.0000, 3.4640])
    V = [v1, v2, v3]

    for v in orthonormalize(V):
        printing(v)


if __name__ == '__main__':
    test()