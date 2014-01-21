#!/usr/bin/python
from ia.ocr.licenseplates.src.create_characters import load_learning_set
from ia.ocr.licenseplates.src.data import exists, DATA_FOLDER
from ia.ocr.licenseplates.src import Classifier


def load_classifier(neighbours, blur_scale, c=None, gamma=None, verbose=0):
    classifier_file = 'classifier_%s_%s.dat' \
            % (blur_scale, neighbours)
    classifier_path = DATA_FOLDER + classifier_file

    if exists(classifier_file):
        if verbose:
            print 'Loading classifier...'

        classifier = Classifier(filename=classifier_path, \
                neighbours=neighbours, verbose=verbose)
    elif c != None and gamma != None:
        if verbose:
            print 'Training new classifier...'

        classifier = Classifier(c=c, gamma=gamma, neighbours=neighbours, \
                verbose=verbose)
        learning_set = load_learning_set(neighbours, blur_scale, \
                verbose=verbose)
        classifier.train(learning_set)
        classifier.save(classifier_path)
    else:
        raise Exception('No soft margin and gamma specified.')

    return classifier


if __name__ == '__main__':
    from sys import argv, exit

    if len(argv) < 3:
        print 'Usage: python %s NEIGHBOURS BLUR_SCALE [ C GAMMA ]' % argv[0]
        exit(1)

    neighbours = int(argv[1])
    blur_scale = float(argv[2])

    # Generate the classifier file
    if len(argv) > 4:
        c = float(argv[3])
        gamma = float(argv[4])
        load_classifier(neighbours, blur_scale, c=c, gamma=gamma, verbose=1)
    else:
        load_classifier(neighbours, blur_scale, verbose=1)
