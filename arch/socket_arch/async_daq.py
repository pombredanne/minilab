from __future__ import print_function

import time
import asyncore
import socket
import sys

# internal
sys.path.append('../../')
from daq.ni.acquisition import AcquisitionTask


class DaqRegister(asyncore.dispatcher):
    """

    """
    device = ''

    def __init__(self, device):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.device = device
        self.status = False

        self.daq = AcquisitionTask(device, 'continuous')
        print('Device %s is initialized' % device['name'])

    def handle_connect(self):
        pass

    def handle_close(self):
        pass

    def handle_expt(self):
        print('fail.')

    def readable(self):
        print(self.daq.read())
        return True

    def writable(self):
        return self.status

    def handle_read(self):
        """

        """
        self.status = True

    def writable(self):
        """

        """
        self.status = False
        self.send('')


def startup(devices):
    server = []
    for name in devices:
        server.append(DaqRegister(devices[name]))

    asyncore.loop(0.0)

if __name__ == '__main__':
    import sys
    import platform

    # internal
    if platform.system() == 'Linux':
        sys.path.append('/var/www/mswim/')
    else:
        sys.path.append('c:/mswim/')

    from util import extract_devices
    from mswim.settings import DEVICES as SENSORS_GROUP

    startup(extract_devices(SENSORS_GROUP))
