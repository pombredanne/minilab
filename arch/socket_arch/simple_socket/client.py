# Echo client program
from __future__ import print_function, division, unicode_literals
from random import randint
import socket
import pickle
import sys
import platform

if platform.system() == 'Linux':
    sys.path.insert(0, '/var/www/mswim')
else:
    sys.path.insert(0, '/mswim/')

from mswim import settings

HOST = 'localhost'    # The remote host
PORT = 50007              # The same port as used by the server


def acquisition_data(type):
    conn_id = str(randint(0, 10**10))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.sendall(pickle.dumps((settings.DEVICES[type], conn_id)))

    breaker = '\n\n\n\n'

    cache = ''
    while True:
        while True:
            cache += s.recv(1024)
            if breaker in cache:
                i = cache.index(breaker)
                data = pickle.loads(cache[:i])
                cache = cache[i+len(breaker):]
                print('Received %s registers.' % len(data))
                del data

    s.close()

acquisition_data('ceramic')