# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 13:59:37 2013

@author: Marcos Gallo
"""

from spectrum import *
from pylab import *
from matplotlib.widgets import Slider, Button
from scipy import signal
import numpy
import time

#freq de muestreo
f = 5000
#tempo entre amostras
T = 1/f
#frequecia de nyquist
nyq = f/2

#lower bound
lb = 2
#upper bound
ub = -1
rawf = open('20130503_093235_piezoQuartzo_DadosBrutos.txt','r')
sinais = []
found = False
for line in rawf:
    if 'X_Value' not in line and not found:
        continue
    if not found: 
        found = True    
        for n in range(len(line.split('\t')[1:-1])):
            sinais.append([])
        continue
    if found:
        for n, val in enumerate(line.split('\t')[1:-1]):
            sinais[n].append(float(val.replace(',','.')))
sinais = [numpy.array(sina) for sina in sinais]

#pego so a primeira sinal
sinal = sinais[0][lb:ub]
n = len(sinal)
k = arange(n)
x1 = arange(n)
x1d = arange(n-1)

#primera derivada
st = time.time()
der = numpy.gradient(sinal,1/5000)
et = time.time()
print 'gradient %s secs' % (et - st)
st = time.time()
der2 = numpy.ediff1d(sinal)
et = time.time()
print 'ediff1d %s secs' % (et  - st)
st = time.time()
der3 = numpy.diff(sinal) #<---- mais rapido! 
et = time.time()
print 'diff %s secs' % (et - st)
#filtro pasa bajos
taps=61
fir_coef = signal.firwin(taps,cutoff=50.0/nyq)
#senial filtrada
sinalf = signal.lfilter(fir_coef,1.0, sinal)

#filtro media movil
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    return (ret[n - 1:] - ret[:1 - n]) / n
mvn = 13
sinalf2 = moving_average(sinal,mvn)
derf = numpy.gradient(sinalf)
#otro filtro
fir2 = signal.firwin(100,cutoff=5.0/nyq)
#pasa alto
fir2 = -fir2
fir2[100/2] = fir2[100/2] + 1
fdiffh = signal.lfilter(fir2,1.0,derf)
#deteccion de zero-crossings
signaldiff = numpy.diff(numpy.sign(der))
signalfdiff = numpy.diff(numpy.sign(derf))

#plots de sinais
subplot(311)
grid()

plot(x1,sinal)
print -taps/2, -taps+taps/2

plot(range(-taps+taps/2,len(sinalf)-taps+taps/2),sinalf)
plot(range(mvn/2,len(sinalf2)+mvn/2),sinalf2)
legend(['o','lp','MA'])
#plots de spectrums
subplot(312)
grid()
p = Periodogram(sinal, f)
p.run()
p.plot()
pf = Periodogram(sinalf, f)
pf.run()
pf.plot()
pfd = Periodogram(sinalf2[:-2 if len(sinalf2)%2 == 0 else -1], f)
pfd.run()
pfd.plot()
legend(['o','lp','MA'])
#plots de derivadas e cruces por zero
subplot(313)
grid()
plot(range(len(der)),der)
plot(range(len(der2)),der2)
plot(range(len(der3)),der3)
#plot(x1, derf)
#plot(x1d, signalfdiff)
#plot(x1,fdiffh)
#plot(range(len(fdiffhz)), fdiffhz)
    
show()
print 'Done'