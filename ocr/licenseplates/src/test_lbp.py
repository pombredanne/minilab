#!/usr/bin/python
from GrayscaleImage import GrayscaleImage
from LocalBinaryPatternizer import LocalBinaryPatternizer

image = GrayscaleImage("/home/ivan/dev/pydev/lab/labtrans/plotter/data/cam/1372180045710-ocr.jpg")

lbp = LocalBinaryPatternizer(image)
histograms = lbp.create_features_vector()

print histograms
