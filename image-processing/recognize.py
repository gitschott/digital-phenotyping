#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the necessary packages
from __future__ import print_function
import numpy as np
import cv2
import math
import argparse
from matplotlib import pyplot as plt
from scipy.signal import argrelextrema
import sys


# Angle-checking function
def is_on_line(x1, y1, x2, y2, x3, y3):
    slope = (y2 - y1) / (x2 - x1)
    return y3 - y1 == slope * (x3 - x1)

# Colour values stretching function
def color_stretch(image):
    for i in range(image.shape[2]):
        image = cv2.equalizeHist(image[:,:,i])
    for index, pixel in np.ndenumerate(image):
        if pixel < 20:
            pixel -= 2
        elif pixel  >230:
            pixel +=3
        else:
            continue

        return image


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
    erosion = cv2.erode(image, kernel, iterations=iterations)
    gray_thin = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)
    gray_thin = cv2.equalizeHist(gray_thin)

    return gray_thin

# Contours selection facilitating function enhanced with the threshold
def contours_selection_threshold(image, iterations):
    #the more iterations, the thinner the contours
    (T, thresh) = cv2.threshold(image, 252, 255, cv2.THRESH_TRUNC)
    kernel = np.ones((5, 5), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=iterations)
    gray_thin = cv2.cvtColor(erosion, cv2.COLOR_BGR2GRAY)

    return gray_thin

# Construct the argument parse and parse the arguments
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="let the process begin")
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    ap.add_argument('-c', '--contours', action='store_true', help="Show image with contours")
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

#contrasting picture by stretching color values
#img = color_stretch(img)

#convert to grayscale, shrink shapes' sizes
gray_thin = contours_selection_threshold(img, 4)
histr = cv2.calcHist(gray_thin,[0],None, [256], [0, 256])

# black_index = int(float(lmsize)*100/float(hsize))
# blo = int(histr[lm_indices[black_index]])
# print(blo)

# Convert to grayscale, shrink shapes' sizes
gray_thin = contours_selection_threshold(img,4)

# cv2.imshow("img", gray_thin)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Find all the 'black' shapes in the image
lower = np.array([0])
upper = np.array([20])
shapeMask = cv2.inRange(gray_thin, lower, upper) #selection of smaller contours

# find the contours in the mask
im, cnts, hier = cv2.findContours(shapeMask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

#If needed: visualization of the contours found
if args['contours'] == True:
    contour_img = np.copy(img)
    cv2.drawContours(contour_img, cnts, -1, (0, 255, 0), thickness=3)


##Geometrical data further can be analyzed in recognition tests
#finding contour areas
areas = []
for c in cnts:
     areas.append(cv2.contourArea(c))

print(type(areas))
max_index = areas.index(max(areas))

#get shape centers
centres = []
for i in range(len(cnts)):
  moments = cv2.moments(cnts[i])
  if moments['m00'] == 0:
      continue
  else:
      centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))

#get the distances between shapes centres
dist = []
coords = []
for (x,y) in centres:
    for (i,j) in centres:
        dist.append(math.hypot(x - i, y - j))
        coords.append((x,y))
dist = np.asarray(dist)

#get the corners coordinates
top = dist.argsort()[-4:][::-1]
top = top.tolist()
corner = []

for i in top:
    corner.append(coords[i])

main_diag_coords = []
p = centres[max_index][0]
q = centres[max_index][1]
for (x,y) in corner:
    for (i,j) in corner:
        iol = is_on_line(x,y,p,q,i,j)
        if iol == True:
             main_diag_coords.append([x,y,i,j])
        else:
            continue

print(type(main_diag_coords))

# Selection of contours, contours mask creation
lst_intensities = []

for c in range(len(cnts)):
    cimg = np.empty_like(img)
    cv2.drawContours(cimg, cnts, c, color=[255,255,255], thickness=-1)
    # Access the image pixels and create a 1D numpy array then add to list
    pts = np.where(cimg == [255,255,255])
    lst_intensities.append(img[pts[1], pts[0]])

colors_avg = []
for i in range(len(lst_intensities)):
    colors_avg.append(np.average(lst_intensities[i], axis=0))

#Checking of the colors recognized (optional)
#for i in main_diag_coords:


#Drawing the colours
c=0
check = np.empty_like(img)
while c<4:
    for t in range(len(colors_avg)):
        if t == max_index:
            pass
        else:
            color = colors_avg[t]
            cv2.drawContours(check, cnts, t, color, thickness=-1)
    c+=1

cv2.imshow("img", contour_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("/Users/apple/tutorial/how_computer_sees.jpg", img)
