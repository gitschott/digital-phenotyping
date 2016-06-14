# import the necessary packages
import numpy as np
np.set_printoptions(threshold=np.nan)
import cv2
import math

##List of constants we know:
diagonal = 160*(2**(-2))

#read the image and its binary
im = cv2.imread('/Users/apple/tutorial/piece.jpg')
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

# find all the 'black' shapes in the image
lower = np.array([0])
upper = np.array([15])
shapeMask = cv2.inRange(gray, lower, upper)
kernel = np.ones((5,5),np.uint8)

# find the contours in the mask
im2, cnts, hier = cv2.findContours(shapeMask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
hier = hier[0]
cv2.drawContours(im, cnts, -1, (0, 255, 0), 2)

#get shapes centers
centres = []
for i in range(len(cnts)):
  moments = cv2.moments(cnts[i])
  centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
  cv2.circle(im, centres[-1], 3, (0, 0, 255), -1)

#get the distances between shapes centres
print(centres[0])
dist = []
start=[]
fin=[]

for (x,y) in centres:
    for (i,j) in centres:
        dist.append(math.hypot(x - i, y - j))
        start.append((i,j))
        fin.append((x,y))

values = np.hstack((start,fin))
print(values[1])
print(type(values))
dist = np.asarray(dist)

bottomright = max(centres,key=lambda item:item[1])
topleft = min(centres, key=lambda item:item)
print(bottomright, topleft)



'''cv2.imshow("Mask", im)
cv2.waitKey(0)
cv2.destroyAllWindows()'''

