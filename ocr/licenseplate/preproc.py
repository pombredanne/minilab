####################################
#Module 2: Image preprocessing
####################################
def preproc(image):
    from opencv.cv import *
    from opencv.highgui import *
    rows = image.rows
    cols = image.cols
    typ = image.type
    binary_image = cvCreateMat(rows,cols,typ)
    cvThreshold(image, binary_image, 100, 100, CV_THRESH_BINARY_INV)
    return binary_image
    #Test case
    #cvStartWindowThread()
    #cvNamedWindow("Binary")
    #cvShowImage("Binary", binary_image)

