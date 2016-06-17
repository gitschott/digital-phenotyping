# import the necessary packages
import numpy as np
np.set_printoptions(threshold=np.nan)
import cv2
import matplotlib.pyplot as plt
from PIL import Image

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

#Get a mask
closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=4)
print(closing.shape)
clopic = np.repeat(closing[:, :, np.newaxis], 3, axis=2)

# find all the 'black' shapes in the image
lower = np.array([0, 0, 0])
upper = np.array([15, 15, 15])
shapeMask = cv2.inRange(clopic, lower, upper)

#find the contours in the mask
im2, cnts, hier = cv2.findContours(shapeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
hier = hier[0]
cv2.drawContours(clopic, cnts, -1, (0, 255, 0), 2)

#get shape centers
centres = []
for i in range(len(cnts)):
  moments = cv2.moments(cnts[i])
  centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
  cv2.circle(im, centres[-1], 3, (0, 0, 255), -1)
  print(centres)


#get the colours
def get_average_color(x, y, n, image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner)
    is (x, y) in the given image"""

    r, g, b = 0, 0, 0
    count = 0
    for s in range(x, x + n + 1):
        for t in range(y, y + n + 1):
            pixlr, pixlg, pixlb = image[s, t]
            r += pixlr
            g += pixlg
            b += pixlb
            count += 1
    return ((r / count), (g / count), (b / count))

#get the avg colour in the centre of a polygon
topleft = []
for i, (x,y) in enumerate(centres):
    x, y = centres[i]
    lr = int(0.1*x)
    td = int(0.1*y)
    topleft.append((int(x-lr),int(y-td)))

rgb = []
for t, (x,y) in enumerate(topleft):
        rgb.append(get_average_color(x,y, 20, im))
        cv2.rectangle(im, (x, y), (x+20, y+20), (0, 255, 0), 3)

print(topleft)
print(len(rgb))

cv2.imshow("Mask", im)
cv2.waitKey(0)
cv2.destroyAllWindows()

 