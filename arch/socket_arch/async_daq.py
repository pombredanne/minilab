from random import random
import asyncore
import socket

# internal
from db import simulate_daq


class DAQ():
    """

    """
    def __init__(self):
        self.devices = None
        self.sensors = None
        self.number_of_channels = 0
        self.daq = None

    def register_devices(self, devices):
        """

        """
        self.devices = devices
        self.sensors = {}
        channels = devices['channels']

        for _id, chans in enumerate(channels):
            self.sensors[_id] = [
                c for c in sorted(
                    chans, key=lambda x: chans[x]
                )
            ]
            self.number_of_channels += len(self.sensors[_id])

        self.daq = simulate_daq()
        self.daq.next()
        self.daq.send(self.sensors[0])

    def read(self):
        return self.read_db()

    def read_db(self):
        return self.daq.next()

    def read_random(self):
        """

        """
        data = []
        for _ in xrange(self.number_of_channels):
            data.append([random() for _ in xrange(1000)])
        return data


class DaqHandler(asyncore.dispatcher_with_send):
    """

    """
    def __init__(self, conn_sock, client_address):
        self.client_address = client_address
        # Create ourselves, but with an already provided socket
        asyncore.dispatcher.__init__(self, conn_sock)
        self.out_buffer = ''
        self.daq = DAQ()

    def handle_read(self):
        data = self.recv(8192)

        if not self.daq.devices:
            self.daq.register_devices(eval(data))

        if data:
            self.send(str(self.daq.read()) + '\n')


class DaqRegister(asyncore.dispatcher):
    """

    """
    device = ''

    def __init__(self, device):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device = device
        self.status = True
        self.daq = DAQ_ACQUISTION

    def readable(self):
        return self.status

    def handle_read(self):
        self.status = False

        self.status = True

server = DaqServer('localhost', 65000)
asyncore.loop()