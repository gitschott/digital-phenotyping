import numpy as np
import cv2

# Create a black image
img = np.zeros((800,800,3), np.uint8)
img[:]=(255,255,255)


 # Draw a rect
 #M
cv2.rectangle(img, (100, 100), (500, 300), (255, 0, 255), -1)
#C
cv2.rectangle(img, (500, 100), (700, 500), (255, 255, 0), -1)
#Y
cv2.rectangle(img, (300, 500), (700, 700), (0, 255, 255), -1)
#Inner
cv2.rectangle(img, (300, 300), (500, 500), (0, 0, 0), 30)
#Outer
cv2.rectangle(img, (100, 100), (700, 700), (0, 0, 0), 30)
##marker
cv2.rectangle(img, (150, 150), (170, 170), (255, 255, 255), -1)
###dots
cv2.rectangle(img, (630, 630), (650, 650), (0, 0, 0), -1)
cv2.rectangle(img, (630, 150), (650, 170), (0, 0, 0), -1)
cv2.rectangle(img, (150, 630), (170, 650), (0, 0, 0), -1)

#Save
cv2.imwrite("/Users/apple/tutorial/palette.jpg", img)
#Display the image
cv2.imshow("img", img)
cv2.waitKey(0)
