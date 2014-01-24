from __future__ import print_function, division
import socket
import pickle

# internal
from generator import gen_data

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

conn, addr = s.accept()

chunk = 1024
breaker = '\n\n\n\n'

sensors, id_conn = pickle.loads(conn.recv(chunk))

print(('Connected by', addr))
while 1:
    for data in gen_data(sensors):
        print('Sent %s registers.' % len(data))
        conn.sendall(pickle.dumps(data, -1) + breaker)

conn.close()