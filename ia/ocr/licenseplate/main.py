from cv import *
#from cv.highgui import *
#from blobs.Blob import *
#from blobs.BlobResult import *
#from Blob import *
#from BlobResult import *
from ia.ocr.licenseplate import preproc, read, resize

image=read()
binary_image=preproc(image)
resize(binary_image)

