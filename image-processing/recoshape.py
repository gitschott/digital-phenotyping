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

    return gray_thin

# Contours selection facilitating function enhanced with the threshold
def contours_selection_threshold(image):
    image = cv2.GaussianBlur(image, (5, 5), 0)  # blur is added to denoise the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret2, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    im, cnts, hier = cv2.findContours(th2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    return cnts

def square_selection(contours, image):
    areas = []
    for c in contours:
        areas.append(cv2.contourArea(c))

    c_areas = np.asarray(areas)
    top = c_areas.argsort()[-2:][::-1]
    a = int(image.shape[0])
    b = int(image.shape[1])
    c = cv2.contourArea(contours[top[0]])

    if c >= 0.97*a*b:
        print('The biggest contour is the picture border, the second biggest contour was selected.')
        top_regime = True
    else:
        print('The biggest contour is not defined properly. The result might be unreliable.')
        top_regime = False

    #selection of second large contour on the picture that is the square
    return top, top_regime

def shrink_the_mask(square_contour, image):
    perimeter = cv2.arcLength(square_contour, True)  # finds closed contour
    if perimeter == 0:
        print('The square is not recognized.')
    epsilon = 0.1 * perimeter
    approx = cv2.approxPolyDP(square_contour, epsilon, True)

    if len(approx) > 4:
        print('The square is not recognized.')

    component = np.zeros_like(image)
    x, y, z, h = approx
    x = x[0]
    z = z[0]
    cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)

    kernel = np.ones((5, 5), np.uint8)
    component = cv2.erode(component, kernel, iterations=6)
    component = cv2.cvtColor(component,cv2.COLOR_BGR2GRAY)
    im, cnts, hier = cv2.findContours(component, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) == 1:
        print('The square is shrinked properly.')

    perimeter = cv2.arcLength(cnts[0], True)  # finds closed contour
    if perimeter == 0:
        print('The square is not recognized.')
    epsilon = 0.1 * perimeter
    approx = cv2.approxPolyDP(cnts[0], epsilon, True)

    if len(approx) > 4:
        print('The square is not recognized.')

    x, y, z, h = approx
    x = tuple(x[0])
    y = tuple(y[0])
    z = tuple(z[0])
    h = tuple(h[0])

    print('There are new coordinates of corners lying inside the contour of the square.')

    return x,y,z,h, component

#def get_the_square(x,y,z,h):
    # x,y,z,h are square corners


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
contours = contours_selection_threshold(img)
top, top_regime = square_selection(contours, img)

# Checkpoint of contour sides
if top_regime == True:
    sq = int(top[1])
else:
    sq = int(top[0])

# Getting the centre of the contour
moments = cv2.moments(contours[sq])
centre = (int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00']))

# Getting the corners and lengths of the sides
topleft, botleft, botright, topright, component = shrink_the_mask(contours[sq], img)

corners = [topleft, botleft, botright, topright]

diag = math.hypot(topleft[0] - botright[0], topleft[1] - botright[1])
wid = math.hypot(topleft[0] - topright[0], topleft[1] - topright[1])
hei = math.hypot(topleft[0] - botleft[0], topleft[1] - botleft[1])

if diag**2 == wid**2+hei**2:
    print('Everything is fine.')

print('The diagonal of the rectangle is %d.' % diag)
print('The width of the rectangle is %d.' % wid)
print('The height of the rectangle is %d.' % hei)

#Selecting the areas for the analysis

x_coef = wid/480
y_coef = hei/480
d_coef = 678.8225099390856 / diag
#white
white = np.zeros_like(img)
white_coords = []


for i in corners:
    if i[0]<300*x_coef:
        x = int(i[0] + 60*x_coef)
        p = int(i[0] + 120*x_coef)
    else:
        x = int(i[0] - 60*x_coef)
        p = int(i[0] - 120*x_coef)
    if i[1]<300*y_coef:
        y = int(i[1] + 60*y_coef)
        q = int(i[1] + 12*y_coef)
    else:
        y = int(i[1] - 60 * y_coef)
        q = int(i[1] - 12 * y_coef)

    white_coords.append(((x,y),(p,q)))
print(white_coords[0])
for i in white_coords:
    cv2.rectangle(white, i[0], i[1], (255, 255, 255), -1)
    white[np.where(white == [255,255,255])] = img[np.where(white == [255,255,255])]


# cv2.drawContours(component, contours, sq, (255,255,255), -1)
cv2.imshow("img", white)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("/Users/apple/digital-phenotyping/test_photos/badwhite.jpg", white)
#finding contour areas


