import sys

sys.path.append('/home/xmn/env/lib/pytesser')

from pytesser import *
import Image
image_path = '/home/xmn/dev/pydev/lab/labtrans/plotter/data/cam/1372180045710-ocr.jpg'
image = Image.open(image_path)  # Open image object using PIL
print image_to_string(image)  # Run tesseract.exe on image
print image_file_to_string(image_path, graceful_errors=True)
