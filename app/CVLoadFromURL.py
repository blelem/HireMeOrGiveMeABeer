import cStringIO
import urllib
import cv2
import PIL
import numpy

def CVLoadFromURL(url):
    ''' Load a file from a url and returns an image file in OpenCV format'''

    file = cStringIO.StringIO(urllib.urlopen(url).read())
    pil_image = PIL.Image.open(file)
    return cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)