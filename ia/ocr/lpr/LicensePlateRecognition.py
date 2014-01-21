# /opt/local/bin/python2
# MacPorts Python 2.7.3
##################################################
# Name:			Tyler Boraski
# Date:			12/11/12
# Class:		CS201
# Assignment:	Final Project - License Plate Recognition
##################################################

# Import libraries
import time
import sys
import copy

# Import OpenCV
import cv

path_root = '/home/ivan/dev/pydev/lab/labtrans/plotter/data/cam/'
image_path = path_root + '20130626_115022_imagemPlaca.jpg'

# OpenCV variables
cv.NamedWindow("CS201 - Tyler Boraski - Final Project", cv.CV_WINDOW_AUTOSIZE)
camera_index = 0
capture = cv.CaptureFromCAM(camera_index)
mhi = None
motionMask = None
orientation = None
prevFrameIndex = 0
buffer = range(10)

# Parameter variables. They can be changed to affect the program
CLOCKS_PER_SEC = 1.0
MHI_DURATION = 0.5
N = 4


##################################################
# Name:         processFrame()
# Description:  Extracts a frame from the webcam
#               and process the image through the
#               motion tracking algorithm.
##################################################
def processFrame():
    # Declare as globals since we are assigning to them now
    global capture
    global camera_index
    global frame_grey
    global prev_frame
    global prev_frame_grey
    global motionMask
    global mhi
    global orientation
    global prevFrameIndex
    diff_threshold = 50

    # Capture current frame
    frame = cv.QueryFrame(capture)

    # Create frame buffer and initial all image variables needed for the motion history algorithm
    if not mhi:
        for i in range(N):
            buffer[i] = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
            cv.Zero(buffer[i])
        mhi = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 1)
        cv.Zero(mhi)
        orientation = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 1)

    # Erode the frame 3 times to remove noise
    #cv.Erode(frame, frame, None, 3)

    # Convert frame to greyscale and store it in the buffer
    cv.CvtColor(frame, buffer[prevFrameIndex], cv.CV_RGB2GRAY)

    # Iterate the indexes of the image buffer
    index1 = prevFrameIndex
    index2 = (prevFrameIndex + 1) % N # Finds the next index in the buffer
    prevFrameIndex = index2
    motionMask = buffer[index2]

    # Find the motion mask by finding the difference between the current and previous frames
    cv.AbsDiff(buffer[index1], buffer[index2], motionMask)

    # Convert the motion mask to a binary image
    cv.Threshold(motionMask, motionMask, diff_threshold, 1, cv.CV_THRESH_BINARY);

    # Produce motion history image
    timeStamp = time.clock() / CLOCKS_PER_SEC
    cv.UpdateMotionHistory(motionMask, mhi, timeStamp, MHI_DURATION)

    # Copy new motion mask onto the motion history image and scale it
    cv.ConvertScale(mhi, motionMask, 255./MHI_DURATION,(MHI_DURATION - timeStamp)*255./MHI_DURATION)

    # Calculate the motion gradient and find the direction of motion
    tempMask = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
    cv.Merge(motionMask, None, None, None, tempMask)
    cv.CalcMotionGradient(mhi, tempMask, orientation, 0.5, 0.05, 3)
    angle = 360 - cv.CalcGlobalOrientation(orientation, tempMask, mhi, timeStamp, MHI_DURATION)
    #print angle

    # Contour detection method
    # Draw motion box and angle line
    cv.Dilate(tempMask, tempMask, None, 1)
    storage = cv.CreateMemStorage(0)
    contour = cv.FindContours(tempMask, storage, cv.CV_RETR_EXTERNAL, cv.CV_CHAIN_APPROX_SIMPLE)
    cv.DrawContours(motionMask, contour, cv.RGB(0, 0, 255), cv.RGB(0, 255, 0), 1) # Change first parameter to motionMask to get mhi and contour

    # Single outermost contour
    """
    try:
        bound_rect1 = contour[0]
        bound_rect2 = contour[1]
        pt1 = (bound_rect1[0], bound_rect1[1])
        pt2 = (bound_rect1[0] + bound_rect2[0], bound_rect1[1] + bound_rect2[1])
        # draw
        cv.Rectangle(motionMask, pt1, pt2, cv.CV_RGB(0,0,255), 1)
    except:
        continue
    """

    # Lots of contours
    """
    while contour:
        bound_rect = cv.BoundingRect(list(contour))
        contour = contour.h_next()
        pt1 = (bound_rect[0], bound_rect[1])
        pt2 = (bound_rect[0] + bound_rect[2], bound_rect[1] + bound_rect[3])

        # draw
        cv.Rectangle(motionMask, pt1, pt2, cv.CV_RGB(0,0,255), 1)
    """
    # Combine motion mask and contours
    output = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
    #cv.Merge(motionMask, None, None, None, tempMask)

    # Display image
    cv.ShowImage("CS201 - Homework 3 - Tyler Boraski", motionMask)

    # If wrong camera index is initialized, press "n" to cycle through camera indexes.
    c = cv.WaitKey(10)
    if c == "n":
        camera_index += 1 				# Try the next camera index
        capture = cv.CaptureFromCAM(camera_index)
        if not capture: 				# If the next camera index didn't work, reset to 0.
            camera_index = 0
            capture = cv.CaptureFromCAM(camera_index)

    # If "esc" is pressed the program will end
    esc = cv.WaitKey(7) % 0x100
    if esc == 27:
        quit()

##################################################
# Name:         templateMatching()
# Description:  Finds a license plate template
##################################################
def templateMatching(template):
    # Declare as globals since we are assigning to them now
    global capture
    global camera_index

    """
    # Create multiple smaller sizes of the template so we find a plate at different distances
    templateList = [0, 0]
    tmp1 = template
    for n in range(2):
        templateList[n] = tmp1
        (w, h) = cv.GetSize(tmp1)
        tmp2 = cv.CreateImage((int(w * 0.5), int(h * 0.5)), cv.IPL_DEPTH_8U, 3)
        cv.Resize(tmp1, tmp2, cv.CV_INTER_LINEAR)
        tmp1 = tmp2
    """

    # Capture current frame
    frame = cv.QueryFrame(capture)

    """
    # Create the temporary images that will hold the comparison results
    frameWidth, frameHeight = cv.GetSize(frame)
    resultList = [0, 0]
    for n in range(2):
        templateWidth, templateHeight = cv.GetSize(templateList[n])
        width = frameWidth - templateWidth + 1
        height = frameHeight - templateHeight + 1
        resultList[n] = cv.CreateImage((width, height), 32, 1)
    """

    frameWidth, frameHeight = cv.GetSize(frame)
    templateWidth, templateHeight = cv.GetSize(template)
    width = frameWidth - templateWidth + 1
    height = frameHeight - templateHeight + 1
    result = cv.CreateImage((width, height), 32, 1)

    # cv.ShowImage("CS201 - Tyler Boraski - Final Project", templateList[0])
    # time.sleep(10)

    # Query for templates
    while True:
        # Capture frame
        frame = cv.QueryFrame(capture)

        # Check for template matchs
        cv.MatchTemplate(frame, template, result, cv.CV_TM_SQDIFF)
        minVal, maxVal, minLoc, maxLoc = cv.MinMaxLoc(result)
        #print minVal
        if minVal < 10000000.0:
            cv.Rectangle(frame, (minLoc[0], minLoc[1]), (minLoc[0] + template.width, minLoc[1] + template.height), cv.CV_RGB(0, 255, 255))


        """
        for n in range(2):
            cv.MatchTemplate(frame, templateList[n], resultList[n], cv.CV_TM_SQDIFF)
            minVal, maxVal, minLoc, maxLoc = cv.MinMaxLoc(resultList[n])
            if n == 0 and minVal < 10000000.0:
                cv.Rectangle(frame, (minLoc[0], minLoc[1]), (minLoc[0] + templateList[n].width, minLoc[1] + templateList[n].height), cv.CV_RGB(255, 255, 255))
            if n == 1 and minVal < 100000000.0:
                cv.Rectangle(frame, (minLoc[0], minLoc[1]), (minLoc[0] + templateList[n].width, minLoc[1] + templateList[n].height), cv.CV_RGB(0, 255, 0))
                print minVal
        """


        # Display image
        cv.ShowImage("CS201 - Tyler Boraski - Final Project", frame)

        # If "esc" is pressed the program will end
        esc = cv.WaitKey(7) % 0x100
        if esc == 27:
            quit()



##################################################
# Main loop of the program. Loops the method
# processFrame() to extract and process a frame
# extracted from the webcam.
##################################################
if  __name__ =='__main__':
    # Load the template
    tmp = cv.LoadImage('templateSmall.jpg', cv.CV_LOAD_IMAGE_UNCHANGED)

    # Run the template matching algorithm
    templateMatching(tmp)