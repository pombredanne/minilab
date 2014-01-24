from random import random


def gen_data(sensors, size=6500):
    """

    """
    cache = []

    while True:
        cache[:] = []
        count = 0
        while count < size:
            cache += [
                random() for _ in sorted(sensors, key=lambda i: sensors[i])
            ]
            count += 1

        yield cache
