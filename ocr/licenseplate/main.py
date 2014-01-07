from cv import *
#from cv.highgui import *
#from blobs.Blob import *
#from blobs.BlobResult import *
#from Blob import *
#from BlobResult import *
from read import read
from preproc import preproc
from resize import resize
image=read()
binary_image=preproc(image)
resize(binary_image)

