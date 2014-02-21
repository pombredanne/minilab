from __future__ import print_function, division
import socket
import asyncore

import platform
import sys
import random

# internal
sys.path.append('../../')

if platform.system() == 'Linux':
    sys.path.append('/var/www/mswim/')
else:
    sys.path.append('c:/mswim/')


class CamHandler(asyncore.dispatcher_with_send):
    """
    Handler used to sends data to DAQ Clients

    """
    def __init__(self, conn_sock, client_address):
        self.client_address = client_address
        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        self.out_buffer = ''
        print('CAM Server initialized')

    def handle_connect(self):
        print('Connection established.')

    def writable(self):
        return True

    def readable(self):
        return True

    def handle_read(self):
        data = self.recv(8192)

        if data:
            data = data.split('\n')[0]
            cmd = data[data.index('=')+1:data.index('&')]

            print(cmd)

            result = ''
            if cmd == 'getid':
                result = '<?xml version="1.0" ?><result>   <location></location>   <cameraid></cameraid>   <ID>1371569907371</ID>   <image_hash>0000</image_hash>   <capture>      <frametime>2013.06.18 15:38:49.146</frametime>      <frametimems>1371569929146</frametimems>      <frameindex>1398</frameindex>   </capture>   <anpr>      <text>&#x6E;&#x2E;&#x61;&#x2E;&#x20;&#x28;&#x35;&#x29;</text>      <type>-1</type>      <frame>0,0,0,0,0,0,0,0</frame>      <bgcolor>0</bgcolor>      <color>0</color>      <confidence>0</confidence>      <timems>0</timems>      <resultcnt>1</resultcnt>   </anpr>   <motdet>      <rect>0,18,90,42</rect>      <confidence>100</confidence>      <objectid>1371569842</objectid>      <objectix>0</objectix>   </motdet>   <control>      <shutterms>100</shutterms>      <again>100</again>      <dgain>100</dgain>      <blacklevel>-19</blacklevel>      <iris>540</iris>   </control>   <trigger>      <speed>-0.01</speed>      <speed_limit>-0.01</speed_limit>      <direction>255</direction>      <category>-1</category>      <timems>0</timems>   </trigger></result>'
            print(result)
            self.send(result)


class CamServer(asyncore.dispatcher):
    """
    Daq Server provides data to DAQ Client from Ring Buffer

    """
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print('DAQ Server initialized')

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            print('Incoming connection from %s' % repr(address))
            handler = CamHandler(sock, address)


def startup(host, port):
    """

    """
    CamServer(host, port)
    asyncore.loop(0.5)


if __name__ == '__main__':
    startup('localhost', 65080)