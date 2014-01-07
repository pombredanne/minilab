# encoding: utf-8
"""
test/characters.py

Testing character extraction.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""
from cv2 import cv
import os
import sys

sys.path.append('../')

import anpr  # @UnresolvedImport
from quick_show import quick_show  # @UnresolvedImport

# files = os.listdir('data/examples')
image_path = '/home/ivan/dev/pydev/lab/labtrans/plotter/data/cam/1372180045710-ocr.jpg'
counter = 0
for f in [image_path]:
	image = cv.LoadImage(f)
	for plate in anpr.detect_plates(image):
		zzz = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 3)
		cv.Smooth(plate, zzz)
		#
		cv.PyrMeanShiftFiltering(plate, zzz, 40, 15)
		foo = anpr.greyscale(plate)
		segmented = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 1)
		bar = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 1)
		cv.EqualizeHist(foo, segmented)
		cv.AdaptiveThreshold(segmented, bar, 255,
			cv.CV_ADAPTIVE_THRESH_GAUSSIAN_C, cv.CV_THRESH_BINARY_INV,
			plate.height % 2 == 0 and (plate.height + 1) or plate.height,
			plate.height / 2)
		baz = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 1)
		el = cv.CreateStructuringElementEx(1, 2, 0, 0, cv.CV_SHAPE_RECT)
		cv.Erode(bar, baz, el)
		quick_show(plate)
		quick_show(segmented)
		quick_show(bar)
		quick_show(baz)
		for char in anpr.find_characters(foo, baz):
			cv.Rectangle(plate, (int(char.x1), int(char.y1)),
				(int(char.x2), int(char.y2)), (255, 0, 0))
		quick_show(plate)
