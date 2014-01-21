###############################################################
# Module 1
# Imports OpenCV libraries and Reads the Image
###############################################################
def read():

    from opencv.cv import *
    from opencv.highgui import *

    print "Importing opencv libraries... Done"

    #Location of the image
    location = "new.JPG" 
    image = cvLoadImageM(location,0)
    return image
    # The lines below are for testing purpose. Un-hash them.
    #cvStartWindowThread()
    #cvShowImage("plate",image)
    #cvNamedWindow("Binary")


