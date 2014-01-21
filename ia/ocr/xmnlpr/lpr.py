# -*- coding: utf-8 -*-
import cv
import os
import cv2

def quick_show(image):
    """Display an image on the screen.

    Quick 'n' dirty method to throw up a window with an image in it and
    wait for the user to dismiss it.
    """
    cv.NamedWindow("foo")
    cv.ShowImage("foo", image)
    cv.WaitKey(0)
    cv.DestroyWindow("foo")

path_root = '/home/ivan/dev/pydev/lab/labtrans/plotter/data/cam/'
path_root = '/media/ivan/bf7f8bb4-842c-4abb-b280-8195370749c0/ivan/dev/labtrans/datos/mswim/placas veiculos/'
# 20130626_115022_imagemPlaca.jpg
for f in os.listdir(path_root):
    #print(type(open(path_root + f).read()))
    #exit()
    #print(f)
    # load
    original = cv.LoadImageM(path_root + f, cv.CV_LOAD_IMAGE_GRAYSCALE)

    # Crop from x, y, w, h -> 100, 200, 100, 200
    cropped = original[0:original.rows-45, 0:original.cols]

    # resize
    thumbnail = cv.CreateMat(
        cropped.rows / 10, cropped.cols / 10, original.type
    )
    cv.Resize(cropped, thumbnail)

    # quick_show(cropped)

    # gray mode
    # CvtColor(original,gray,CV_RGB2GRAY)
    #gray = cv.CreateImage((original.width, original.height), cv.IPL_DEPTH_8U, 1)
    #cv.CvtColor(original,gray,cv.CV_RGB2GRAY)

    # localize
    # cvThreshold(image, binary_image,128,255, CV_THRESH_OTSU)
    threshes = {'otsu': cv.CV_THRESH_OTSU,
                'binary': cv.CV_THRESH_BINARY,
                'binary_inv': cv.CV_THRESH_BINARY_INV,
                'trunk': cv.CV_THRESH_TRUNC,
                'tozero': cv.CV_THRESH_TOZERO,
                'tozero_inv': cv.CV_THRESH_TOZERO_INV}
    threshes_available = ['otsu', 'binary']
    for name, thresh in threshes.items():
        if name not in threshes_available:
            continue
        print(name)
        binary_image = cv.CreateMat(
            cropped.rows, cropped.cols, original.type
        )
        color = 255
        threshold = 128
        cv.Threshold(cropped, binary_image, threshold, color, thresh)

        quick_show(binary_image)

        # Connected Component Analysis
        #myblobs = cv2.CBlobResult(binary_image, mask, 0, True)
        #myblobs.filter_blobs(325,2000)
        #blob_count = myblobs.GetNumBlobs()

    quick_show(thumbnail)
