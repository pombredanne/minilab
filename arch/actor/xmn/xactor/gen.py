# -*- coding: utf-8 -*-
# Echo server program
import socket
import random

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()

print 'Connected by', addr
while True:
    data = random.randint(0, 100)
    conn.sendall(str(data))
conn.close()