import numpy
import sys
import json
from PIL import Image


def __editImage(imagepath, color):
    image = Image.open(imagepath)
    image = numpy.array(image)

    x = {"r": {1, 2}, "g": {0, 2}, "b": {0, 1}}
    for value in x[color]:
        image[:, :, value] *= 0
    return Image.fromarray(image)


def main():
    """
    Modify an image

    Keyword arguments:
    inpath -- path to input image
    jsonpath -- path to input argument json file
    outpath -- where to save output image
    """
    inpath = sys.argv[1]
    jsonpath = sys.argv[2]
    outpath = sys.argv[3]

    args = json.loads(open(jsonpath, 'r').read())

    image = __editImage(inpath, args['color'])
    image.save(outpath)


if __name__ == "__main__":
    main()
