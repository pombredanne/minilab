# -*- coding: utf-8 -*-
from reader import wim
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import EngFormatter

labwim = wim('/home/ivan/dev/pydev/labtrans/mswim/data/20130401_110658_piezoQuartzo_DadosBrutos.txt')
dados = labwim.extrai_dados()

"Configuração do gráfico"

formatter = EngFormatter(unit='s', places=1)
plt.grid(True)

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
    
plt.show()