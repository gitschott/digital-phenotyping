#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import the necessary packages
import numpy as np
import cv2
import math
import argparse

#get the colours
def get_average_color(image):
    """ 3-tuple containing the BGR value
    of the average color of masque,
     ignoring zero values"""

    r, g, b = 0, 0, 0
    count = 0
    for index, pixel in np.ndenumerate(image):
        if pixel == 0:
            blacks +=1
        else:
            s,t = index
            pixlb, pixlg, pixlr = image[s,t]
            if pixlb <= pixlg <= pixlr <= 1:
                count += 0
            else:
                b += pixlb
                g += pixlg
                r += pixlr
                count += 1
    return ((r / count), (g / count), (b / count))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Hello. Upload the picture for the analysis please.')
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

args = parser.parse_args()
print(args.accumulate(args.integers))

#read the image and convert it to acceptable array for analysis
img = cv2.imread(args["image"]) #image for analysis
bin = cv2.imread(args["image"],0) #binary of an image
img = cv2.GaussianBlur(img,(5,5),0)

#convert to grayscale, shrink shapes' sizes
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 4)
gray_thin = cv2.cvtColor(erosion,cv2.COLOR_BGR2GRAY)

# find all the 'black' shapes in the image
lower = np.array([0])
upper = np.array([15])
#shapeMask = cv2.inRange(gray, lower, upper)
shapeMask = cv2.inRange(gray_thin, lower, upper) #selection of smaller contours

# find the contours in the mask
im, cnts, hier = cv2.findContours(shapeMask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

#If needed: visualize the contours found
##Do not use this when analyzing color values
#cv2.drawContours(img, cnts,-1, (0,255,0), thickness=3)

#finding contour areas (optional)
# areas = []
# for c in cnts:
#     areas.append(cv2.contourArea(c))
#
# max_index = np.argmax(areas)

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
max_index = areas.index(max(areas)) #selects the contour with the biggest area
cnt=cnts[max_index] #selects coordinates of the biggest contour

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

cv2.imshow("img", check)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("/Users/apple/tutorial/how_computer_sees.jpg", img)
