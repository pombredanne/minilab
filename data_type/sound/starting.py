# -*- coding: utf-8 -*-
import numpy as np
import math
import pylab


def plota(size, omega):
    data = []
    for n in range(size):
        data.append(math.sin(n*omega))
    pylab.plot(data)
    pylab.show()

plota(100, math.pi*2)