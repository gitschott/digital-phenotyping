#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the necessary packages
import numpy as np
import cv2
import math
import argparse
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from scipy.signal import argrelextrema
from scipy.stats import norm
import sys

# Angle-checking function
def is_on_line(x1, y1, x2, y2, x3, y3):
    # integer class variables expected
    slope = (y2 - y1) / (x2 - x1)
    return y3 - y1 == slope * (x3 - x1)

# Color values stretching acccording to the histogram
def histogram_stretch(image):
    # an RGB image is required to perform the analysis
    for i in range(image.shape[2]):
        blue = image[:,:,i]
        blue = cv2.equalizeHist(blue)
        image[:,:,i] = blue
    return image

# Contours selection facilitating function
def contours_selection(image, iterations):
    #the more iterations, the thinner the contours
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(gray, kernel, iterations=iterations)
    gray_thin = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
    gray_thin = cv2.equalizeHist(gray_thin)

    return gray_thin

# Contours selection facilitating function enhanced with the threshold
def contours_selection_threshold(image, iterations):
    #the more iterations, the thinner the contours
    (T, thresh) = cv2.threshold(image, 250, 255, cv2.THRESH_TRUNC)
    kernel = np.ones((5, 5), np.uint8)
    print(thresh.shape)
    erosion = cv2.erode(thresh, kernel, iterations=iterations)
    gray_thin = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)

    return gray_thin

def is_contour_bad(c):
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # the contour is 'bad' if it is not a rectangle
    return not len(approx) == 4

# Construct the argument parse and parse the arguments
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="let the process begin")
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    ap.add_argument('-p', '--panic', action='store_true', help="Show every image on each step")
    args = vars(ap.parse_args())
    # ap = argparse.ArgumentParser(description ="Upload of the picture for the analysis, specify some details.")
    # ap.add_argument('-i','--image', required=True, help="Path to the image file")
    # # ap.add_argument('-c', '--contours', stored='store_true', help="Show image with contours")
    # # ap.add_argument('-i', '--save', stored='store_true', help="Save the result")
    # # args = vars(ap.parse_args(['-i','-c','-s']))
    # args = ap.parse_args()
    # print(args)
    # print(args[image])


 # Read the image and convert it to acceptable array for analysis
img = cv2.imread(args['image'])  # image for analysis
img = cv2.GaussianBlur(img,(5,5),0)  #blur is added to denoise the image

# Cutting the contours of the black frame
frame = np.copy(img)
ret3,th4 = cv2.threshold(frame,100,256,cv2.THRESH_BINARY)

if args['panic'] == True:
    cv2.imshow("img", th4)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Making the picture binary
gray = cv2.cvtColor(th4, cv2.COLOR_BGR2GRAY)

if args['panic'] == True:
    cv2.imshow("img", gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Selecting minimum pixel value
rango = np.unique(gray)

# Creating a mask
mask = np.zeros_like(gray) # Create mask where white is what we want, black otherwise
mask[gray == rango[0]] = 255
ret3,th4 = cv2.threshold(mask,100,256,cv2.THRESH_BINARY_INV)

if args['panic'] == True:
    cv2.imshow("img", th4)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# find the contours in the mask
im, cnts, hier = cv2.findContours(th4, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

#finding contour areas
areas = []
for c in cnts:
    areas.append(cv2.contourArea(c))



max_index = areas.index(np.max(areas))

# Selection of contours, contours mask creation
lst_intensities = []
count = 0
for c in range(len(cnts)):
    cimg = np.zeros_like(img)
    if is_contour_bad(cnts[c]):
        continue
    else:
        cv2.drawContours(cimg, cnts, c, color=[255,255,255], thickness=-1)
        # Access the image pixels and create a 1D numpy array then add to list
    pts = np.where(cimg == [255,255,255])
    lst_intensities.append(img[pts[0], pts[1]])

# Obtaining average intensity values
colors_avg = []
for i in range(len(lst_intensities)):
    colors_avg.append(np.average(lst_intensities[i], axis=0))

# Drawing the colours, checking the averages
if args['panic'] == True:
    c=0
    check = np.empty_like(img)
    while c<4:
        for t in range(len(colors_avg)):
            if t >= max_index-1:
                pass
            else:
                color = colors_avg[t]
                cv2.drawContours(check, cnts, t, color, thickness=-1)
        c+=1
    cv2.drawContours(check, cnts, -1, [0,255,0], thickness=5)

    cv2.imshow("img", check)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #cv2.imwrite("/Users/apple/tutorial/how_computer_sees.jpg", img)


# Analyzing the white balance
##Whites are the squares in the corners

#get shapes centers according to 'image moments'
centres = []
for i in range(len(cnts)):
  moments = cv2.moments(cnts[i])
  print(moments['m00'])
  if moments['m00'] != 0:
      centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))

  # get the distances between shapes centres
  dist = []
  coords = []
  for (x, y) in centres:
      for (i, j) in centres:
          dist.append(math.hypot(x - i, y - j))
          coords.append((x, y))
  dist = np.asarray(dist)

  # get the corners coordinates
  top = dist.argsort()[-4:][::-1]
  top = top.tolist()
  corner = []

  for i in top:
      corner.append(coords[i])

print(corner)
cv2.circle(check, corner[-1], 3, (0, 255, 0), -1)
cv2.imshow("img", check)
cv2.waitKey(0)
cv2.destroyAllWindows()
# for c in colors_avg:
#     for i in range(len(c)):
#         print(int(c[i]))

### I AM NOT YET SURE HOW TO RECOGNIZE THE WHITE SQUARES

