# -*- coding: utf-8 -*-
"""
Visualiza datos en gráficos utilizando la librería google charts

"""

import matplotlib.pyplot as plt
import numpy as np
import random

from matplotlib.ticker import EngFormatter

sample = 2
sensors = [random.sample(xrange(100), sample), 
           random.sample(xrange(100), sample),
           random.sample(xrange(100), sample),
           random.sample(xrange(100), sample),
           random.sample(xrange(100), sample),
           random.sample(xrange(100), sample),
           random.sample(xrange(100), sample)]
dados = np.array(sensors)

"Configuração do gráfico"

print(sensors)

formatter = EngFormatter(unit='s', places=1)
plt.grid(True)
"""
"Analisa os sensores"
for sensor in dados:
    ax = plt.subplot(111)
    ax.xaxis.set_major_formatter(formatter)
    xs = []
    ys = []

    "Analisa os tempos do sensor"
    for tempo in sorted(dados[sensor].keys()):
        xs.append(tempo)
        ys.append(dados[sensor][tempo])

    ax.plot(xs, ys)
"""
ax = plt.subplot(111)
ax.xaxis.set_major_formatter(formatter)
ax.plot([.1,.2,.3,.4,.5,.6,.7],dados)

plt.show()