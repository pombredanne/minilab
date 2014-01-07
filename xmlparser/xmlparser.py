# -*- coding: utf-8 -*-
import sys
# append location of mswim module
#sys.path.append('/home/ivan/dev/pydev/labtrans/mswim/')
sys.path.append('c:/dev/labtrans/mswim/')

from devices.cam2 import FXCamd102
    
cam = FXCamd102('192.168.1.97')
#cam.send_trigger(True)
#im = cam.image()
#open('cam.jpg', 'wb').write(im)
lplate = cam.license_plate(1372115751681)

print('License Plate: %s' % lplate)
print(cam.time(1372115751681))