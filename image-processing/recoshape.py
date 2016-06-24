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

# Contours selection facilitating function enhanced with the threshold
def contours_selection_threshold(image):
    image = cv2.GaussianBlur(image, (5, 5), 0)  # blur is added to denoise the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret2, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    tresh = np.copy(th2)
    im, cnts, hier = cv2.findContours(th2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    return cnts,tresh

def square_selection(contours, image):
    areas = []
    a = int(image.shape[0])
    b = int(image.shape[1])
    for c in contours:
        areas.append(cv2.contourArea(c))

    c_areas = np.asarray(areas)
    top = c_areas.argsort()[-2:][::-1]
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
    mask = np.zeros_like(image)

    if len(approx) == 2:
        print("It is a square!")
        square = True
        x,z = approx
        x = x[0]
        y = (0,0)
        z = z[0]
        h = (0,0)
        cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
        component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
        cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        c = 0
        for (l,m), unit in np.ndenumerate(component):
            if component[l, m] == mask[l, m]:
                c += 0
            else:
                c += 1

        if c > image.shape[0] * image.shape[1] * 0.97:
            print('Your square fits perfectly.')
            checkpoint = True
        else:
            print('The square is rotated or distorted.')
            checkpoint = False

    else:
        square = False
        x,y,z,h = approx
        x = tuple(x[0])
        y = tuple(y[0])
        z = tuple(z[0])
        h = tuple(h[0])

        cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
        cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
        component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        print('There are new coordinates of corners lying inside the contour of the square.')

        if mask[x[1], x[0]] == 255:
            print('Your square fits perfectly.')
            checkpoint = True
        else:
            print('The square is rotated or distorted.')
            checkpoint = False

    return x, y, z, h, mask, component, square, checkpoint


def geometry_of_white(image, list_of_corners, width, height):
    x_coef = width / 480
    y_coef = height / 480
    # d_coef = diag / 678.8225099390856

    white = np.zeros_like(image)
    white_coords = []

    for i in corners:
        if i[0] < centre[0]:
            x = int(i[0] + 60 * x_coef)
            p = int(i[0] + 120 * x_coef)
            if i[1] < centre[1]:
                y = int(i[1] + 60 * y_coef)
                q = int(i[1] + 120 * y_coef)
            else:
                y = int(i[1] - 60 * y_coef)
                q = int(i[1] - 120 * y_coef)
        else:
            x = int(i[0] - 60 * x_coef)
            p = int(i[0] - 120 * x_coef)
            if i[1] < centre[1]:
                y = int(i[1] + 60 * y_coef)
                q = int(i[1] + 120 * y_coef)
            else:
                y = int(i[1] - 60 * y_coef)
                q = int(i[1] - 120 * y_coef)

        white_coords.append(((x, y), (p, q)))

    for i in white_coords:
        cv2.rectangle(white, i[0], i[1], (255, 255, 255), -1)

    pts = np.where(white == [255, 255, 255])

    x = pts[0]
    y = pts[1]

    wh = []
    for i in range(len(x)):
        wh.append((x[i], y[i]))

    intensities = []
    for i in range(len(wh)):
        x, y = wh[i]
        intensities.append(image[x, y])
        white[x, y] = intensities[i]

    whites = np.unique(white)

    return whites, intensities, white

def info(array):
    a = print(type(array))
    b = print(array[0])
    c = print(array.shape)

    return a,b,c

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
a,b,c = info(img)
print(a,b,c)
contours,th2 = contours_selection_threshold(img)
top, top_regime = square_selection(contours, img)

# Checkpoint of contour sides
if top_regime == True:
    sq = int(top[1])
else:
    sq = int(top[0])

topleft, botleft, botright, topright, mask, component, square, checkpoint = shrink_the_mask(contours[sq], img)

if square == True:
    botleft = (topleft[0], botright[1])
    topright = (botright[0], topleft[1])
    corners = [topleft, botleft, botright, topright]
else:
    corners = [topleft, botleft, botright, topright]

# Getting the centre of the contour
moments = cv2.moments(contours[sq])
centre = (int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00']))

diag = math.hypot(float(topleft[0]) - float(botright[0]), float(topleft[1]) - float(botright[1]))
wid = math.hypot(float(topleft[0]) - float(topright[0]), float(topleft[1]) - float(topright[1]))
hei = math.hypot(float(topleft[0]) - float(botleft[0]), float(topleft[1]) - float(botleft[1]))

if diag**2 == wid**2+hei**2:
    print('Everything is fine.')

print('The diagonal of the rectangle is %d.' % diag)
print('The width of the rectangle is %d.' % wid)
print('The height of the rectangle is %d.' % hei)



whites, intensities, white = geometry_of_white(img,corners, wid, hei)

white_av = sum(whites)/(len(whites)-1)

for i in range(len(whites)):
    if i == 0:
        pass
    else:
        a = round(whites[i]/white_av)
        c = 0
        if a !=1:
            c+=1

if c > 0:
    print("White areas are not recognized.")
else:
    print("White is white. Let it be.")


# cv2.drawContours(component, contours, sq, (255,255,255), -1)
cv2.imshow("img", white)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("/test_images/badwhite3.jpg", white)
#finding contour areas


