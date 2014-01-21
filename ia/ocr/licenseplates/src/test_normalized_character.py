#!/usr/bin/python
from ia.ocr.licenseplates.src import GrayscaleImage, NormalizedCharacterImage

image = GrayscaleImage("../images/test10.png")
normalized_character_image = NormalizedCharacterImage(image)
normalized_character_image.show()
