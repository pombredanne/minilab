from PIL import Image
import sys

import pyocr
import pyocr.builders

image_path = '/home/xmn/dev/pydev/lab/labtrans/plotter/data/cam/1372180045710-ocr.jpg'

tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
for tool in tools:
    print("Will use tool '%s'" % (tool.get_name()))
    # Ex: Will use tool 'tesseract'

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[0]
    print("Will use lang '%s'" % (lang))
    # Ex: Will use lang 'fra'

    txt = tool.image_to_string(Image.open(image_path),
                               lang=lang,
                               builder=pyocr.builders.TextBuilder())
    word_boxes = tool.image_to_string(Image.open(image_path),
                                      lang=lang,
                                      builder=pyocr.builders.WordBoxBuilder())
    line_and_word_boxes = tool.image_to_string(
            Image.open(image_path), lang=lang,
            builder=pyocr.builders.LineBoxBuilder())


    print txt
    print
    for wb in word_boxes:
        print wb
    print
    for lwb in line_and_word_boxes:
        print lwb
