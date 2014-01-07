
#!/usr/bin/env python
# encoding: utf-8
"""
test/plates.py

Testing plate detection.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""

import os
import sys
import cv

sys.path.append('../')
import anpr
from quick_show import quick_show
path_root = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/placas veiculos/'
image_path = '/home/ivan/dev/pydev/lab/labtrans/plotter/data/cam/1372180045709.jpg'

#files = os.listdir('data/examples')
counter = 0
for f in os.listdir(path_root):
	image = cv.LoadImage(path_root + f)
	for plate in anpr.detect_plates(image):
		cv.SaveImage('output%02d.png' % counter, plate)
		counter = counter+1