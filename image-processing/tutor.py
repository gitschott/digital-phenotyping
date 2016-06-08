#import numpy as np
#import scipy


#from skimage import data, color, util
#pic = img_as_float(np.arrange('/Users/apple/git/digital-phenotyping/digital-phenotyping/skin_new/yLWt1vanqmI.jpg'))
#>>> coins = data.coins()
#>>> histo = np.histogram(coins, bins=np.arange(0, 256)
import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')
import numpy as np
from PIL import Image
from numpy import unravel_index

#import argparse
#import cv2
#import matplotlib.pyplot as plt
import os, os.path
from glob import glob


im = Image.open("/Users/apple/tutorial/set/tumblr_o72jmrfSkl1rvapjbo1_500.jpg")
#filelist = glob('*.jpg')
#filelist.sort()
print(type(im))

pic = np.asarray(im)
print(type(pic))
#pix = im.load()
#print(pic.shape, pic.dtype, "-- This is input image characteristics")  # Get the width and hight of the image for iterating over

pic = pic[:,0:450,:]

#m = pix[214, 202]
#e = pix[334, 44]

#print(m, e, "The first is white, the second is black.")

'''for i in range(li):
    im_%i = Image.open("/Users/apple/tutorial/set/*.jpg")
    filelist = glob('*.jpg')
    filelist.sort()
    print(type(im_%i))

    pic_%i = np.asarray(im_%i)
    print(type(pic_%i))'''


#image_data_blue = image_data[:,:,2]

#median_blue = np.median(image_data_blue)

#non_empty_columns = np.where(image_data_blue.max(axis=0)>median_blue)[0]
#non_empty_rows = np.where(image_data_blue.max(axis=1)>median_blue)[0]

#boundingBox = (min(non_empty_rows), max(non_empty_rows), min(non_empty_columns), max(non_empty_columns))

pix = im.load()
print(pic.shape, pic.dtype, "-- This is input image characteristics") #Get the width and hight of the image for iterating over
hist = np.histogram(pic, bins=np.arange(0, 256))

for i in pic:
    m = pic.argmax()
    e = pic.argmin()

m_i = unravel_index(m, pic.shape)
e_i = unravel_index(e, pic.shape)



oo = pix[214,202]
ee = pix[334,44]

print(m_i,e_i, "The first is white, the second is black.")

#how to parse the args
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", help = "path to the image file")
#args = vars(ap.parse_args())

# load the image
#pic = cv2.imread(args["/Users/apple/tutorial/test.jpg"])

# find the white shape in the image
#lower = np.array([14, 0, 0])
#upper = np.array([15, 15, 15])
#shapeMask = cv2.inRange(image, lower, upper)

