# encoding: utf-8
"""
test/characters.py

Testing character extraction.

Created by Oliver Smith on 2009-09-26.
Copyright (c) 2009 Oliver Smith. All rights reserved.
"""
import os
import sys

from cv2 import cv
from ia.ocr.OpenANPR.test import quick_show


sys.path.append('OpenANPR/')
sys.path.append('OpenANPR/test')
sys.path.append('/home/ivan/env/lib/pytesser')

import anpr  # @UnresolvedImport

import pyocr
import pyocr.builders

from pytesser import *

def adjust_license(text):
    text = text.replace(' ', '')
    text1 = text[:3]
    text2 = text[3:]

    text1 = text1.replace('1', 'I')
    text1 = text1.replace('0', 'O')
    text2 = text2.replace('I', '1')
    text2 = text2.replace('O', '0')

    return text1 + text2

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)

path_root = '/home/ivan/dev/pydev/lab/labtrans/plotter/data/cam/'
# 20130626_115022_imagemPlaca.jpg
for f in os.listdir(path_root):
    #for f in ['20130626_115022_imagemPlaca.jpg']:
    print f
    image = cv.LoadImageM(path_root + f)
    for plate in anpr.detect_plates(image):
        #quick_show(image)
        #quick_show(plate)
        #zzz = cv.CreateImage(cv.GetSize(plate), cv.IPL_DEPTH_8U, 3)
        #cv.Smooth(plate, zzz)
        #
        #cv.PyrMeanShiftFiltering(plate, zzz, 40, 15)
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
        # quick_show(plate)
        print 'baz'
        quick_show(baz)
        print 'bar'
        quick_show(bar)
        print 'segmented'
        quick_show(segmented)
        image_path = 'plate.png'
        image_path2 = 'plate2.png'

        cv.SaveImage(image_path, foo)

        for tool in tools:
            print("Will use tool '%s'" % (tool.get_name()))
            # Ex: Will use tool 'tesseract'

            langs = tool.get_available_languages()
            print("Available languages: %s" % ", ".join(langs))
            lang = 'eng'
            print("Will use lang '%s'" % (lang))
            # Ex: Will use lang 'fra'

            txt = tool.image_to_string(
                Image.open(image_path),
                lang=lang,
                builder=pyocr.builders.TextBuilder()
            )
            """
            word_boxes = tool.image_to_string(
                Image.open(image_path),
                lang=lang,
                builder=pyocr.builders.WordBoxBuilder())
            line_and_word_boxes = tool.image_to_string(
                Image.open(image_path), lang=lang,
                builder=pyocr.builders.LineBoxBuilder())
            """
            print txt, '>>', adjust_license(txt)
            """
            print
            for wb in word_boxes:
                print '>>>', wb
            print
            for lwb in line_and_word_boxes:
                print '>>>>', lwb
            """
            print ''

            original = cv.LoadImageM(image_path, cv.CV_LOAD_IMAGE_GRAYSCALE)

            binary_image = cv.CreateMat(
                original.rows, original.cols, original.type
            )
            color = 255
            threshold = 128
            cv.Threshold(original, binary_image, threshold, color, cv.CV_THRESH_OTSU)
            print('otsu')
            quick_show(binary_image)
            cv.SaveImage(image_path2, binary_image)
            txt = tool.image_to_string(
                Image.open(image_path2),
                lang=lang,
                builder=pyocr.builders.TextBuilder()
            )
            print '>>%s' % txt
# png
# lang eng
# cuneiform bar: HKQ 3 I 42
# teserract bar: fuxiﬁtizj
# cuneiform plate: none
# teserract plate: none
# cuneiform segmented: none
# tesseract segmented: none
# tesseract baz: (m<if:aT42j
# cuneiform baz: IIKO JI 42

# jpg
# lang eng
# cuneiform bar: g NK Q 3 I 42+
# teserract bar:
# cuneiform plate: none
# teserract plate: none
# cuneiform segmented: none
# tesseract segmented: none
# tesseract baz: (m<if:aT42j
# cuneiform baz: IIKO JI 42