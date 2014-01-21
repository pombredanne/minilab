# -*- coding: utf-8 -*-
import numpy as np
from matplotlib import pyplot

t = np.linspace(-1, 1, 1000)

"""
# Ex 1
x = np.cos(1*np.pi*t)
y = np.cos(5*np.pi*t)

pyplot.plot(x)
pyplot.plot(y)
pyplot.plot(x+y)

"""

"""
# DOC
Vector plots can also be made in Matplotlib. Here is a script producing a vector plot and a key showing the scale of the vectors:

>>> x = linspace(0,10,11)
>>> y = linspace(0,15,16)
>>> (X,Y) = meshgrid(x,y)
>>> u = 5*X
>>> v = 5*Y
>>> q = plt.quiver(X,Y,u,v,angles='xy',scale=1000,color='r')
>>> p = plt.quiverkey(q,1,16.5,50,"50 m/s",coordinates='data',color='r')
>>> xl = plt.xlabel("x (km)")
>>> yl = plt.ylabel("y (km)")
>>> plt.show()
"""

"""
# Ex 2
x = np.array([0, 0, 3, 2])
y = np.array([0, 0, 9, 9])
z = x + y

vecs =np.array([x, y, z])
X,Y,U,V = zip(*vecs)

print X
print Y
print U
print V

ax = pyplot.gca()
ax.quiver(X,Y,U,V,angles='xy',scale_units='xy',scale=1)
ax.set_xlim([-1,20])
ax.set_ylim([-1,20])
pyplot.draw()

pyplot.grid()
pyplot.show()
"""

"""
# DOC 2

# implement the example graphs/integral from pyx
from pylab import *
from matplotlib.patches import Polygon

def func(x):
    return (x-3)*(x-5)*(x-7)+85

ax = subplot(111)

a, b = 2, 9 # integral area
x = arange(0, 10, 0.01)
y = func(x)
plot(x, y, linewidth=1)

# make the shaded region
ix = arange(a, b, 0.01)
iy = func(ix)
verts = [(a,0)] + list(zip(ix,iy)) + [(b,0)]
poly = Polygon(verts, facecolor='0.8', edgecolor='k')
ax.add_patch(poly)

text(0.5 * (a + b), 30,
     r"$\int_a^b f(x)\mathrm{d}x$", horizontalalignment='center',
     fontsize=20)

axis([0,10, 0, 180])
figtext(0.9, 0.05, 'x')
figtext(0.1, 0.9, 'y')
ax.set_xticks((a,b))
ax.set_xticklabels(('a','b'))
ax.set_yticks([])
show()

"""

"""
# Ex 3

# implement the example graphs/integral from pyx
from matplotlib.patches import Polygon

def _x(t):
    return np.sin(np.pi*t)

def _y(t):
    return t


def calc1(t):
    return x + y

ax = pyplot.subplot(111)

a, b = -0.5, 0.5 # integral area

t = np.linspace(-1, 1, 1000)

x = _x(t)
y = _y(t)

pyplot.plot(t, x, linewidth=1)
pyplot.plot(t, y, linewidth=1)
pyplot.plot(t, x * y)
pyplot.plot(t, x * x)

print np.dot(x, x)*2/t.size
print np.sum(x * x)*2/t.size

# make the shaded region
#ix = np.arange(a, b, 0.0001)
#iy = np.sin(ix*np.pi)
#verts = [(a,0)] + list(zip(ix,iy)) + [(b,0)]
#poly = Polygon(verts, facecolor='0.8', edgecolor='k')

#ax.add_patch(poly)

#pyplot.text(0.5 * (a + b), 30,
#     r"$\int_a^b f(x)\mathrm{d}x$", horizontalalignment='center',
#     fontsize=20)

pyplot.axis([-1,1, -2, 2])
pyplot.grid()
#pyplot.figtext(0.9, 0.05, 'x')
#pyplot.figtext(0.1, 0.9, 'y')
#ax.set_xticks((a,b))
#ax.set_xticklabels(('a','b'))
#ax.set_yticks([])
pyplot.show()

"""

"""
# Ex 4
t = np.linspace(-1, 1, 1000)
x = lambda t: np.sin(t*np.pi)
y = lambda t: 1 - np.abs(t)

pyplot.plot(t, x(t), linewidth=2)
pyplot.plot(t, y(t), linewidth=2)
pyplot.plot(t, x(t) * y(t))

print np.dot(x(t), y(t))

pyplot.axis([-1,1, -2, 2])
pyplot.grid()
pyplot.show()

"""

"""
# Ex 5
t = np.linspace(-1, 1, 1000)
x = lambda t: np.sin(4*np.pi*t)
y = lambda t: np.sin(5*np.pi*t)

pyplot.plot(t, np.zeros(t.size), linewidth=4)
pyplot.plot(t, x(t), linewidth=2)
pyplot.plot(t, y(t), linewidth=2)
pyplot.plot(t, x(t) * y(t))

print np.dot(x(t), y(t))

pyplot.axis([-1,1, -2, 2])
pyplot.grid()
pyplot.show()

"""

# Ex 6

_x = lambda t: \
    np.sin(4*np.pi*t.astype(complex))

_y = lambda t: \
    np.sin(5*np.pi*t.astype(complex))

def _sum(x, y, N):
    x_star = x.conjugate()
    # 0 to N-1 (-1 in range is implicity)
    return sum([x_star[n] * y[n] for n in range(N)])

t = np.linspace(-1, 1, 100000)

x = _x(t)
y = _y(t)

print((np.dot(x, y), np.dot(y, x)))
print(_sum(x, y, t.size))

pyplot.plot(t, np.zeros(t.size), linewidth=4)
pyplot.plot(t, _x(t), linewidth=2)
pyplot.plot(t, _y(t), linewidth=2)
pyplot.plot(t, _x(t) * _y(t), linewidth=2)
pyplot.axis([-1,1, -2, 2])
pyplot.grid()
pyplot.show()

# formal properties
# <x + y, y> = <x, z> * <y, x>
# <x, y> = <y, x>*
# <alpha * x, y> = alpha* * <x, y>
# <x, alpha * y> = alpha * <x, y>

# <x, y> = sum (x*)[n] * y[n], n=0 to N-1


exit()