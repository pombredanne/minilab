from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import PolyCollection
from matplotlib.colors import colorConverter
import matplotlib.pyplot as plt
import numpy as np
from reader import wim

labwim = wim('C:/dev/pyenv/project/mswim/data/20130503_100145_piezoQuartzo_DadosBrutos.txt')
dados = labwim.extrai_dados()

fig = plt.figure()
ax = fig.gca(projection='3d')
cc = lambda arg: colorConverter.to_rgba(arg, alpha=0.6)

zs = []
verts = []
colors = []
x_max = 0
y_max = 0

"Analisa os sensores"
for sensor in dados:
    xs = []
    ys = []
    zs.append(sensor)

    "Analisa os tempos do sensor"
    for tempo in sorted(dados[sensor].keys()[:20]):
        xs.append(tempo)
        ys.append(dados[sensor][tempo])
        x_max = max([x_max, tempo])
        y_max = max([y_max, dados[sensor][tempo]])

    colors.append(cc('r'))
    verts.append(list(zip(xs, ys)))

poly = PolyCollection(verts, facecolors = colors)
poly.set_alpha(0.7)
ax.add_collection3d(poly, zs=zs, zdir='y')

ax.set_xlabel('Tempo')
ax.set_xlim3d(0, 3)
ax.set_ylabel('Tensao')
ax.set_ylim3d(0, len(zs)-1)
ax.set_zlabel('Sensor')
ax.set_zlim3d(0, 3)

plt.show()