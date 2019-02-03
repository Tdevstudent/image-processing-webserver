import sys
from PIL import Image


def main():
    """
    Return input image

    Keyword arguments:
    inpath -- path to input image
    jsonpath -- path to input argument json file
    outpath -- where to save output image
    """
    inpath = sys.argv[1]
    outpath = sys.argv[3]

    image = Image.open(inpath)
    image.save(outpath)


if __name__ == "__main__":
    main()
