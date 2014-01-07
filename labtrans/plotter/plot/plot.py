# -*- coding: utf-8 -*-
from reader import wim
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import EngFormatter

labwim = wim('C:/pyenv/projects/mswim/data/20130503_100145_piezoQuartzo_DadosBrutos.txt')
dados = labwim.extrai_dados()

"Configuração do gráfico"

formatter = EngFormatter(unit='s', places=1)

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
    break