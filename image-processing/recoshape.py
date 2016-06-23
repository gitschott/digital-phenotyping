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

if top_regime == True:
    sq = int(top[1])
else:
    sq = int(top[0])

moments = cv2.moments(contours[sq])
centre = (int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00']))
print(centre)
print(moments)

#finding contour areas


