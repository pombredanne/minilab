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


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 65080              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

chunk = 1024

while True:
    conn, addr = s.accept()

    print(('Connected by', addr))

    data = conn.recv(chunk)
    data = data.split('\n')[0]

    try:
        cmd = data[data.index('=')+1:data.index('&')]
    except:
        cmd = data[data.index('=')+1:data.index(' H')]

    print(cmd)

    result = ''
    photo_id = str(random.randint(0, 1000000000))
    print(photo_id)
    if cmd == 'getid':
        result = (
            '<result>   <location></location>   ' +
            '<cameraid></cameraid>   <ID>' + photo_id + '</ID>   ' +
            '<image_hash>0000</image_hash>   <capture>      ' +
            '<frametime>2013.06.18 15:38:49.146</frametime>      ' +
            '<frametimems>1371569929146</frametimems>      ' +
            '<frameindex>1398</frameindex>   </capture>   <anpr>      ' +
            '<text>&#x6E;&#x2E;&#x61;&#x2E;&#x20;&#x28;&#x35;&#x29;' +
            '</text><type>-1</type>      ' +
            '<frame>0,0,0,0,0,0,0,0</frame><bgcolor>0</bgcolor>    ' +
            '  <color>0</color><confidence>0</confidence>' +
            '<timems>0</timems><resultcnt>1</resultcnt></anpr>' +
            '<motdet><rect>0,18,90,42</rect><confidence>100</confidence>' +
            '<objectid>1371569842</objectid><objectix>0</objectix>' +
            '</motdet><control><shutterms>100</shutterms>' +
            '<again>100</again>      <dgain>100</dgain>' +
            '<blacklevel>-19</blacklevel><iris>540</iris></control>' +
            '<trigger><speed>-0.01</speed><speed_limit>-0.01' +
            '</speed_limit><direction>255</direction><category>-1' +
            '</category>      <timems>0</timems>   </trigger></result>'
        )
    elif cmd == 'sendtrigger':
        result = (
            '<result>   <location></location>   ' +
            '<cameraid></cameraid>   <ID>' + photo_id + '</ID>   ' +
            '<image_hash>0000</image_hash>   <capture>      ' +
            '<frametime>2013.06.18 15:38:49.146</frametime>      ' +
            '<frametimems>1371569929146</frametimems>      ' +
            '<frameindex>1398</frameindex>   </capture>   <anpr>      ' +
            '<text>&#x6E;&#x2E;&#x61;&#x2E;&#x20;&#x28;&#x35;&#x29;' +
            '</text><type>-1</type>      ' +
            '<frame>0,0,0,0,0,0,0,0</frame><bgcolor>0</bgcolor>    ' +
            '  <color>0</color><confidence>0</confidence>' +
            '<timems>0</timems><resultcnt>1</resultcnt></anpr>' +
            '<motdet><rect>0,18,90,42</rect><confidence>100</confidence>' +
            '<objectid>1371569842</objectid><objectix>0</objectix>' +
            '</motdet><control><shutterms>100</shutterms>' +
            '<again>100</again>      <dgain>100</dgain>' +
            '<blacklevel>-19</blacklevel><iris>540</iris></control>' +
            '<trigger><speed>-0.01</speed><speed_limit>-0.01' +
            '</speed_limit><direction>255</direction><category>-1' +
            '</category>      <timems>0</timems>   </trigger></result>'
        )
    elif cmd == 'getimage':
        f = open(
            '../../ocr/licenseplates/docs/' +
            '00991_000000.jpg', 'rb'
        )
        result = f.read()
        f.close()
    elif cmd == 'getdata':
        result = (
            '<result>   <location></location>   ' +
            '<cameraid></cameraid>   <ID>' + photo_id + '</ID>   ' +
            '<image_hash>0000</image_hash>   <capture>      ' +
            '<frametime>2013.06.18 15:38:49.146</frametime>      ' +
            '<frametimems>1371569929146</frametimems>      ' +
            '<frameindex>1398</frameindex>   </capture>   <anpr>      ' +
            '<text>&#x6E;&#x2E;&#x61;&#x2E;&#x20;&#x28;&#x35;&#x29;' +
            '</text><type>-1</type>      ' +
            '<frame>0,0,0,0,0,0,0,0</frame><bgcolor>0</bgcolor>    ' +
            '  <color>0</color><confidence>0</confidence>' +
            '<timems>0</timems><resultcnt>1</resultcnt></anpr>' +
            '<motdet><rect>0,18,90,42</rect><confidence>100</confidence>' +
            '<objectid>1371569842</objectid><objectix>0</objectix>' +
            '</motdet><control><shutterms>100</shutterms>' +
            '<again>100</again>      <dgain>100</dgain>' +
            '<blacklevel>-19</blacklevel><iris>540</iris></control>' +
            '<trigger><speed>-0.01</speed><speed_limit>-0.01' +
            '</speed_limit><direction>255</direction><category>-1' +
            '</category>      <timems>0</timems>   </trigger></result>'
        )

    response_headers = {
        'Content-Type': 'text/html; encoding=utf8',
        'Content-Length': len(result),
        'Connection': 'close',
    }

    response_headers_raw = ''.join\
        ('%s: %s\n' % (k, v) for k, v in response_headers.iteritems()
    )

    # Reply as HTTP/1.1 server, saying "HTTP OK" (code 200).
    response_proto = 'HTTP/1.1'
    response_status = '200'
    response_status_text = 'OK'  # this can be random

    # sending all this stuff
    """
    conn.send(
        '%s %s %s' % (response_proto, response_status, response_status_text)
    )"""

    #conn.send(response_headers_raw)
    #conn.send('\n')  # to separate headers from body
    conn.send(result)

    conn.close()


