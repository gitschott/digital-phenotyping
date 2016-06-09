# import the necessary packages
import numpy as np
import cv2
import matplotlib.pyplot as plt

#read the image and its binary
im = cv2.imread('/Users/apple/tutorial/palette_on_skin.jpg')
bw = cv2.imread('/Users/apple/tutorial/palette_on_skin.jpg', 0)
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

# find all the 'black' shapes in the image
lower = np.array([0])
upper = np.array([15])
shapeMask = cv2.inRange(bw, lower, upper)
kernel = np.ones((5,5),np.uint8)

# find the contours in the mask
im2, cnts, mas = cv2.findContours(shapeMask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Initialize empty list of intensities
lst_int = []

# For each list of contour points...
for i in range(len(cnts)):
# Create a mask image that contains the contour filled in
    bg = np.zeros_like(bw)
    cv2.drawContours(bg, cnts, i, color=255, thickness=-1)

#Mask WHITE
res = cv2.bitwise_and(im,im,mask = bg)
gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

T, thresh = cv2.threshold(gray, 252, 255, cv2.THRESH_BINARY)

#Select white
white = np.copy(thresh)

#Rm withe dot
im3, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
sh = bw.shape
for cnt in contours:
    if cv2.contourArea(cnt)<sh[0]*10:
        if cv2.contourArea(cnt) >100:
                cv2.drawContours(gray,[cnt],0,255,-1)
                # Build a ROI to crop the QR
                x, y, w, h = cv2.boundingRect(cnt)
                white_mask = cv2.rectangle(white, (x,y),(x+w,y+h),(0,0,0),-1)

white = cv2.bitwise_and(im,im,mask = white_mask)

tmp_mask = np.copy(white)
tmp_mask[tmp_mask==0]=1
tmp_mask[tmp_mask>250]=0
tmp_mask[tmp_mask==1]=255
tmp_mask = cv2.erode(tmp_mask,kernel,iterations = 7)

res_w =np.copy(res)
indices = np.where(np.all(tmp_mask==0,axis=-1))
coords = zip(indices[0], indices[1])

for c in coords:
    res_w[c]=0

###Mask YELLOW
gray = cv2.cvtColor(res_w,cv2.COLOR_RGB2GRAY)

ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
yellow = np.copy(thresh)

cv2.imshow("Image", yellow)
cv2.waitKey(0)
cv2.destroyAllWindows()