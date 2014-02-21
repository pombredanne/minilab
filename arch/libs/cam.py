from __future__ import print_function, division
import socket
import pickle

import platform
import sys

# internal
sys.path.append('../../')

if platform.system() == 'Linux':
    sys.path.append('/var/www/mswim/')
else:
    sys.path.append('c:/mswim/')

from labtrans.devices.cam import FXCamd102


def main():
    cam = FXCamd102('localhost:65080')
    imageid = cam.send_trigger(True)
    im = cam.image(imageid)
    open('%s.jpg' % imageid, 'wb').write(im)
    lplate = cam.license_plate(imageid)

    print('License Plate: %s' % lplate)
    print(cam.time(imageid))


if __name__ == '__main__':
    main()