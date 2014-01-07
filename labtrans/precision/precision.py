#!/usr/bin/python
 
import sys
 
# using mpmath for arbitrary precision, 
# sympy for showing the equation in pretty way
if sys.platform == 'linux2':
        import mpmath as mp, sympy as sm
elif sys.platform == 'win32':
        import sympy as sm
        mp = sm.mpmath
 
# just for write shorter code
f = mp.mpf
ms = mp.nstr
pr = sm.pprint
 
print 'Equation for testing arbitrary precision'
# show the equation with pretty printing
pr(173746*sm.sin(1e22) + 94228*sm.log(17.1) - 78487*sm.exp(0.42))
 
# Expected value from the reference 'Why and how to use arbitrary precision'
# by Kaveh R. Ghazi, Vincent Lefevre, Philippe Theveny, Paul Zimmermann
expect = '-1.3418189578296195e-12'
 
# show default setting for mpmath
print '\n Default', mp.mp, '\n'
 
print 'Expected value are', expect, '\n'
print 'Searching prec value, to match the expected value', expect
# calc -> calculate ; cpr -> for comparing with previosly calculated
calc = cpr = 0  
 
# loop for searching prec setting that matched 
# expected value -1.341818958e-12'
# by calculating f_1 function
while calc != expect:
        mp.mp.prec +=1
        a, b, c = mp.sin(1e22), mp.log(f('17.1')), mp.exp(f('0.42'))
        r = f(173746)*(a) + f(94228)*(b) - f(78487)*(c)
        calc = mp.nstr(r, n=17)
        if cpr != calc:
            cpr = calc
        # uncomment below to find out when the calculated is changed
        # than previous when prec is changed
            #print cpr, mp.mp   
 
print 'Found Significand', mp.mp
print 'Result using above setting =', calc
print 'mpmath backend', mp.libmp.BACKEND #show mpmath backend