from ia.ocr.licenseplates.src.xml_helper_functions import xml_to_LicensePlate

for i in range(9):
    for j in range(100):
        try:
            filename = '%04d/00991_%04d%02d' % (i, i, j)
            print 'loading file "%s"' % filename
            plate = xml_to_LicensePlate(filename, save_character=1)
        except:
            print 'epic fail'