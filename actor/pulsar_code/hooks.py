from functools import partial
from pulsar import spawn, TcpServer

import pulsar

def create_echo_server(address, actor):
    '''Starts an echo server on a newly spawn actor'''
    server = TcpServer(actor.event_loop, address[0], address[1],
                       EchoServerProtocol)
    yield server.start_serving()
    actor.servers['echo'] = server
    actor.extra['echo-address'] = server.address

arbiter = pulsar.arbiter()
proxy = spawn(start=partial(create_echo_server, 'localhost:9898'))