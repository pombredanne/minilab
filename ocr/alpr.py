#! /usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

import pymeanshift as pms

from blobs.BlobResult import CBlobResult
from blobs.Blob import CBlob  # Note: This must be imported in order to destroy blobs and use other methods


#############################################################################
# so, here is the main part of the program

if __name__ == '__main__':

    import sys
    import os
    
    blob_overlay = True

    file_name = "plates/license1.png"
    if len(sys.argv) != 1:
        file_name = sys.argv[1]
    
    base_name = os.path.basename(file_name)

    fname_prefix = ".".join(base_name.split(".")[:-1])
    print fname_prefix


    # Image load & conversion to cvmat
    license_plate = cv2.imread(file_name, cv2.CV_LOAD_IMAGE_COLOR)

    # Segment
    segmented, labels, regions = pms.segment(license_plate, 3, 3, 50)
    print "Segmentation results"
    print "%s: %s" % ("labels", labels)
    print "%s: %s" % ("regions", regions)
    cv2.imwrite('%s_segmented.png' % fname_prefix, segmented)


    license_plate = cv2.imread('%s_segmented.png' % fname_prefix, cv2.CV_LOAD_IMAGE_COLOR)

    license_plate_size = (license_plate.shape[1], license_plate.shape[0])

    license_plate_cvmat = cv2.cv.fromarray(license_plate)
    license_plate_ipl = cv2.cv.CreateImage(license_plate_size, cv2.cv.IPL_DEPTH_8U, 3)
    cv2.cv.SetData(
            license_plate_ipl,
            license_plate.tostring(),
            license_plate.dtype.itemsize * 3 * license_plate.shape[1])


    license_plate_white_ipl = cv2.cv.CreateImage(license_plate_size, cv2.cv.IPL_DEPTH_8U, 1)
    cv2.cv.Set(license_plate_white_ipl, 255)
   
    # Grayscale conversion
    inverted_license_plate_grayscale_ipl = cv2.cv.CreateImage(
            license_plate_size,
            cv2.cv.IPL_DEPTH_8U, 1)

    license_plate_grayscale_ipl = cv2.cv.CreateImage(
            license_plate_size,
            cv2.cv.IPL_DEPTH_8U, 1)
    cv2.cv.CvtColor(
            license_plate_cvmat,
            license_plate_grayscale_ipl,
            cv2.COLOR_RGB2GRAY);
    license_plate_grayscale_np = np.asarray(license_plate_grayscale_ipl[:,:])
    # We can also use cv.saveimage
    # cv2.cv.SaveImage('license1_grayscale.png', license_plate_grayscale_ipl)
    cv2.imwrite('%s_grayscale.png' % fname_prefix, license_plate_grayscale_np)

    # Thresholding or binarization of images
    (threshold_value, thresh_image) = cv2.threshold(
            license_plate_grayscale_np,
            128,
            255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print "Thresholding complete. Partition value is %d" % threshold_value
    cv2.imwrite('%s_threshold.png' % fname_prefix, thresh_image)
    
    # Create a mask that will cover the entire image
    mask = cv2.cv.CreateImage (license_plate_size, 8, 1)
    cv2.cv.Set(mask, 1)

	#if not blob_overlay:
	#	# Convert black-and-white version back into three-color representation
	#	cv2.cv.CvtColor(my_grayscale, frame_cvmat, cv2.COLOR_GRAY2RGB);
	
    # Blob detection
    thresh_image_ipl = cv2.cv.CreateImage(license_plate_size, cv2.cv.IPL_DEPTH_8U, 1)
    cv2.cv.SetData(
            thresh_image_ipl,
            thresh_image.tostring(),
            thresh_image.dtype.itemsize * 1 * thresh_image.shape[1])


    cv2.cv.Not(thresh_image_ipl, inverted_license_plate_grayscale_ipl)

    # Min blob size and Max blob size
    min_blob_size = 100 # Blob must be 30 px by 30 px
    max_blob_size = 10000
    threshold = 100

    # Plate area as % of image area:
    max_plate_to_image_ratio = 0.3
    min_plate_to_image_ratio = 0.01
    image_area = license_plate_size[0] * license_plate_size[1]

    # Mask - Blob extracted where mask is set to 1
    # Third parameter is threshold value to apply prior to blob detection
    # Boolean indicating whether we find moments
    myblobs = CBlobResult(thresh_image_ipl, mask, threshold, True)
    myblobs.filter_blobs(min_blob_size, max_blob_size)
    blob_count = myblobs.GetNumBlobs()
    print "Found %d blob[s] betweeen size %d and %d using threshold %d" % (
            blob_count, min_blob_size, max_blob_size, threshold)

    for i in range(blob_count):

        my_enumerated_blob = myblobs.GetBlob(i)
#        print "%d: Area = %d" % (i, my_enumerated_blob.Area())
        my_enumerated_blob.FillBlob(
                license_plate_grayscale_ipl,
                #license_plate_ipl,
                #cv2.cv.Scalar(255, 0, 0),
                cv2.cv.CV_RGB(255, 0, 0),
                0, 0)
        my_enumerated_blob.FillBlob(
                license_plate_white_ipl,
                #license_plate_ipl,
                #cv2.cv.Scalar(255, 0, 0),
                cv2.cv.CV_RGB(255, 255, 255),
                0, 0)


    # we can now save the image
    #annotated_image = np.asarray(license_plate_ipl[:,:])
    blob_image = np.asarray(license_plate_grayscale_ipl[:,:])
    cv2.imwrite("%s_blobs.png" % fname_prefix, blob_image)

    blob_white_image = np.asarray(license_plate_white_ipl[:,:])
    cv2.imwrite("%s_white_blobs.png" % fname_prefix, blob_white_image)

    # Looking for a rectangle -  Plates are rectangular
    # Thresholding image, the find contours then approxPolyDP
    (threshold_value, blob_threshold_image) = cv2.threshold(
            blob_white_image,
            128,
            255,
            cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print "Thresholding complete. Partition value is %d" % threshold_value
    cv2.imwrite('%s_blob_threshold.png' % fname_prefix, blob_threshold_image)
 
    # Blur to reduce noise?
    #blurred_plate = cv2.GaussianBlur(blob_threshold_image, (5,5), 0)
    #blob_threshold_image = blurred_plate
 
    # Erode then dilate to reduce noise
    blob_threshold_image_invert = cv2.bitwise_not(blob_threshold_image)
    cv2.imwrite("%s_pre_dilated_and_eroded.png" % fname_prefix, blob_threshold_image_invert)
    eroded_white_blobs = cv2.erode(blob_threshold_image_invert, None, iterations=4);
    cv2.imwrite("%s_eroded_image.png" % fname_prefix, eroded_white_blobs)

    dilated_white_blobs = cv2.dilate(eroded_white_blobs, None, iterations=4);
    cv2.imwrite("%s_dilated.png" % fname_prefix, dilated_white_blobs)

    blob_threshold_image = cv2.bitwise_not(blob_threshold_image_invert)
    cv2.imwrite("%s_dilated_and_eroded.png" % fname_prefix, blob_threshold_image)

    blob_threshold_image_invert = cv2.bitwise_not(blob_threshold_image)
    contours, hierarchy = cv2.findContours(
            blob_threshold_image,
            cv2.RETR_LIST,
            cv2.CHAIN_APPROX_SIMPLE)
    #print "Contours: ", contours

    # We now have contours. Approximate the polygon shapes
    largest_rectangle_idx = 0
    largest_rectangle_area = 0
    rectangles = []
    colours = ( (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255))
    for idx, contour in enumerate(contours):
	print "Contour: %d" % idx
        contour_area = cv2.contourArea(contour)

        if float(contour_area / image_area) < min_plate_to_image_ratio:
            print "Contour %d under threshold. Countour Area: %f" % (idx, contour_area)
            continue
        elif float(contour_area / image_area) > max_plate_to_image_ratio:
            print "Contour %d over threshold. Countour Area: %f" % (idx, contour_area)
            continue

        approx = cv2.approxPolyDP(
                contour,
                0.02 * cv2.arcLength(contour, True),
                True)

        print "\n -"
        print "%d. Countour Area: %f, Arclength: %f, Polygon %d colour:%s" % (idx,
                contour_area,
                cv2.arcLength(contour, True),
                len(approx),
                colours[idx%len(colours)])
        minarea_rectangle = cv2.minAreaRect(contour)
        minarea_box = cv2.cv.BoxPoints(minarea_rectangle)
        print "> ", minarea_rectangle
        print ">> ", minarea_box
        centre, width_and_height, theta = minarea_rectangle
        aspect_ratio =  float(max(width_and_height) / min(width_and_height))
        print " aspect ratio: %f for %s " % (aspect_ratio, width_and_height)
    	
	minarea_box = np.int0(minarea_box)
    	cv2.drawContours(license_plate, [minarea_box], 0, (255,0,255), 2)
   
        cv2.drawContours(
            license_plate,
            [contours[idx]],
            0,
            colours[idx%len(colours)])
    
        # Aspect ratio removal
        if aspect_ratio < 3 or aspect_ratio > 5:
            print " Aspect ratio bounds fails"
            continue

        # Rectangles have polygon shape 4
        if len(approx) == 4:
            # Select the largest rect
            rectangles.append(contour)
            if contour_area > largest_rectangle_area :
                largest_rectangle_area = contour_area
                largest_rectangle_idx = idx

    print "Probable plate hit is %d" % largest_rectangle_idx
    cv2.drawContours(
            license_plate,
            [contours[largest_rectangle_idx]],
            0,
            colours[0],
            idx + 1)
    
    cv2.imwrite("%s_contours_colored.png" % fname_prefix, license_plate)

    # Create a mask for the detected plate
    #hull = cv2.convexHull(contours[largest_rectangle_idx])
    
    # This bounding rectangle does not consider rotation
    license_plate = cv2.imread(file_name, cv2.CV_LOAD_IMAGE_COLOR)
    bounding_rectangle = cv2.boundingRect(contours[largest_rectangle_idx])
    b_rect_x, b_rect_y, b_rect_w, b_rect_h = bounding_rectangle
    plate_rectangle = (b_rect_x, b_rect_y,  b_rect_w,  b_rect_h)
    print "Plate rectangle is: ", plate_rectangle
    cv2.rectangle(license_plate, (b_rect_x, b_rect_y), (b_rect_x + b_rect_w, b_rect_y + b_rect_h), (0, 255, 0), 2)
    cv2.imwrite("%s_bounding_box.png" % fname_prefix, license_plate)

    license_plate = cv2.imread(file_name, cv2.CV_LOAD_IMAGE_COLOR)
    minarea_rectangle = cv2.minAreaRect(contours[largest_rectangle_idx])
    minarea_box = cv2.cv.BoxPoints(minarea_rectangle)
    minarea_box = np.int0(minarea_box)
    cv2.drawContours(license_plate, [minarea_box], 0, (0,0,255), 2)
    cv2.imwrite("%s_bounding_box_minarea.png" % fname_prefix, license_plate)

