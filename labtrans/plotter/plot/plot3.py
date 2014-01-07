# -*- coding: utf-8 -*-
"""
Visualiza datos en gráficos utilizando la librería google charts

"""
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
graphic = [['DDP', 'Tempo']]
graphic[0] += ['sensor %s' % x for x in range(1, 32)]

xs = []
linea = []
tempo_captado = False

for sensor in dados:
    ys = []
    
    "Analisa os tempos do sensor"
    for tempo in sorted(dados[sensor].keys()[:1000]):
        if not tempo_captado: xs.append(float(tempo))
        ys.append(float(dados[sensor][tempo]))
    
    if not tempo_captado: linea.append(xs)
    linea.append(ys)
    tempo_captado = True
        

#tempo = 15000
#print len(xs)

graphic += map(lambda l: list(l), zip(*linea))  
output = open('plot-template.html').read().replace(
    '{{data}}', '%s' % graphic).replace(
    '],', '],\n')
graphic = None


open('plot.html', 'w').write(output)