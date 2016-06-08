# import the necessary packages

import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i', "--image", help="/Users/apple/tutorial")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["test.jpg"])

# find all the 'black' shapes in the image
lower = np.array([14, 14, 14])
upper = np.array([15, 15, 15])
shapeMask = cv2.inRange(image, lower, upper)

# find the contours in the mask
(cnts, _) = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print("I found %d shapes" % (len(cnts)))
cv2.imshow("Mask", shapeMask)

# loop over the contours
for c in cnts:
    # draw the contour and show it
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)