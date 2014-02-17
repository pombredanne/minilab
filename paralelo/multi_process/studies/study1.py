# -*- coding: utf-8 -*-
"""
Consideraciones:

1 - Pool
Con la estructura normal no se puede pasar un método como referencia:
 -> result = pool.apply_async(_c.f, [10])
 -> pool.map(_c.f, range(10))
    Error info: PicklingError: Can't pickle
    <type 'instancemethod'>: attribute lookup
    __builtin__.instancemethod failed

 Este problema se da por la incompatibilid en pickle, que
 necesita de que las variables estén definidas como globales.

 Otro problema que puede suceder es cuando la clase utiliza generators:
  -> pool.map(run_server, servers)
     PicklingError: Can't pickle <type 'generator'>:
     attribute lookup __builtin__.generator failed

 Soluciones:

 1 - Dejar el objeto como público (fuera del escopo) y llamarlo dentro de la
 función.

 2 - Enviar como argumento el objeto y sus argumentos:
   -> pool.map(p, map(lambda x: (_c, x), range(10)))
   El problema de esta solución es cuando se necesita utilizar y cambiar
   valores de atributos internos, pues, posiblemente, no sufrirá todos los
   cambios esperados (ej. del retorno de una función incremental
   [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]).


2 - Process y Queues
Procesos y queues funcionan bien con objetos:
 -> p = Process(target=g, args=(q, daq))  # q=Queue(), daq=DAQ(), g is a def


"""
from multiprocessing import Pool, Queue, Process
from time import sleep


def g(x):
    sleep(1)
    print x
    return x*x


def f(x):
    sleep(0.1)
    print x
    return x*x

if __name__ == '__main__':
    pool = Pool(processes=4)              # start 4 worker processes
    result = pool.apply_async(g, [11])    # evaluate "f(10)" asynchronously
    print 'hi'
    #print result.get(timeout=2)           # prints "100" unless your computer is *very* slow
    print 'hi2'
    print pool.map(f, range(10))          # prints "[0, 1, 4,..., 81]"
    print 'hi3'
    sleep(1)