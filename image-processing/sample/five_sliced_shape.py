import numpy as np
import cv2

# Create a black image
img = np.zeros((600,600,3), np.uint8)
img[:]=(0,0,0)

#list parameters of shapes:
border = 20 # width of the borders
sq = 100 #side of the white square
color = 40 #side of CMY rectangle

#draw first side
c=0
while c<4:
    x=100
    y=100
    cv2.rectangle(img, (x,y), (x+sq,y+sq), (255, 255, 255), -1)
    cyan = x+sq+border
    cv2.rectangle(img, (cyan, y), (cyan+color, y + sq), (255, 255, 0), -1)
    yellow = cyan+color+border
    cv2.rectangle(img, (yellow, y), (yellow + color, y + sq), (0, 255, 255), -1)
    magenta = yellow+color+border
    cv2.rectangle(img, (magenta, y), (magenta+color, y + sq), (255, 0, 255), -1)
    cols, rows, dims = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    img = cv2.warpAffine(img,M,(cols,rows))
    c+=1

# Draw a white frame
cv2.rectangle(img, (0,0), (600,600), (255, 255, 255), 120)
cv2.rectangle(img, (220,220), (380,380), (255, 255, 255), -1)

##List of constants we know:
diagonal = 160*(2**(-2))

#Save
cv2.imwrite("~/digital-phenotyping/image-processing/sample/piece.jpg", img)
#Display the image
cv2.imshow("img", img)
cv2.waitKey(0)
