# import the necessary packages
import numpy as np
np.set_printoptions(threshold=np.nan)
import cv2
import math

#read the image and convert it to grayscale
img = cv2.imread('/Users/apple/tutorial/piece_on skin_rotS_noise5.jpg')
bin = cv2.imread('/Users/apple/tutorial/piece_on skin_rotS_noise5.jpg',0)
img = cv2.GaussianBlur(img,(5,5),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
kernel = np.ones((5,5),np.uint8)
erosion = cv2.erode(img,kernel,iterations = 2)
gray_thin = cv2.cvtColor(erosion,cv2.COLOR_BGR2GRAY)

# find all the 'black' shapes in the image
lower = np.array([0])
upper = np.array([15])
#shapeMask = cv2.inRange(gray, lower, upper)
shapeMask = cv2.inRange(gray_thin, lower, upper)

# find the contours in the mask
im, cnts, hier = cv2.findContours(shapeMask, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# Find the index of the largest contour

#cv2.drawContours(img, cnts,-1, (0,255,0), thickness=3)

areas = []
for c in cnts:
    areas.append(cv2.contourArea(c))

# Initialize empty list
lst_intensities = []

# For each list of contour points...
for c in range(len(cnts)):
    # Create a mask image that contains the contour filled in
    cimg = np.zeros_like(img)
    cv2.drawContours(cimg, cnts, c, color=[255,255,255], thickness=-1)
    # Access the image pixels and create a 1D numpy array then add to list
    pts = np.where(cimg == [255,255,255])
    lst_intensities.append(img[pts[1], pts[0]])

print((pts[0]).shape)
print(type(pts))

#get the colours
def get_average_color(image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner)
    is (x, y) in the given image"""

    r, g, b = 0, 0, 0
    count = 0
    for index, pixel in np.ndenumerate(image):
        if pixel == 0:
            print("Blackie!")
        else:
            s,t = index
            pixlb, pixlg, pixlr = image[s,t]
            if pixlb == pixlg == pixlr == 0:
                pass
            else:
                b += pixlb
                g += pixlg
                r += pixlr
                count += 1
    return ((r / count), (g / count), (b / count))

colors_avg = []
for i in range(len(lst_intensities)):
    colors_avg.append(np.average(lst_intensities[i], axis=0))


print(colors_avg)
max_index = areas.index(max(areas))
cnt=cnts[max_index]

'''hier = hier[0] #get the hierarchy of contours values

#info on contours
x, y, w, h = cv2.boundingRect(cnt)
print(x,y,w,h)
aspect_ratio = float(w) / h
print("Aspect ratio: %d" % aspect_ratio)

area = cv2.contourArea(cnt)
rect_area = w*h
extent = float(area)/rect_area
print("Extent: %d" % extent)

max_index = np.argmax(area)
border_cont=cnts[max_index]
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area
print("Solidity: %d" % solidity)

equi_diameter = np.sqrt(4*area/np.pi)
(x,y),(MA,ma),orangle = cv2.fitEllipse(cnt)

mask = np.zeros(gray.shape,np.uint8)
cv2.drawContours(mask,cnts,0,255,-1)
pixelpoints = np.transpose(np.nonzero(mask))
#pixelpoints = cv2.findNonZero(mask)

min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(gray,mask = mask)
mean_val = cv2.mean(img,mask = mask)

# leftmost = tuple(cnts[cnts[:,:,0].argmin()][0])
# rightmost = tuple(cnts[cnts[:,:,0].argmax()][0])
# topmost = tuple(cnts[cnts[:,:,1].argmin()][0])
# bottommost = tuple(cnts[cnts[:,:,1].argmax()][0])

# cv2.drawContours(img, ctk, -1, (0, 255, 0), 2)

#get shapes centers according to 'image moments'
centres = []
for i in range(len(cnts)):
  moments = cv2.moments(cnts[i])
  centres.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
  #cv2.circle(img, centres[-1], 3, (0, 0, 255), -1)

#get the distances between shapes centres
dist = []
coords = []
for (x,y) in centres:
    for (i,j) in centres:
        dist.append(math.hypot(x - i, y - j))
        coords.append((x,y))
dist = np.asarray(dist)

#get the corners coordinates
top = dist.argsort()[-4:][::-1]
top = top.tolist()
corner = []

for i in top:
    corner.append(coords[i])

#get main diagonals and 4 sides middles
diag = []
for (x,y) in corner:
    for (i,j) in corner:
        diag.append(math.hypot(x - i, y - j))

diag = list(set(diag))
print(diag)

#check if any coefficient/rotation is needed
#constants of the shape pattern
BORDER = 20 # width of the borders
SQUARE = 100 #side of the white square
COLOR = 40 #side of CMY rectangle
DISTANCE = SQUARE+4*BORDER+3*COLOR

#angle-checking function
def is_on_line(x1, y1, x2, y2, x3, y3):
    slope = (y2 - y1) / (x2 - x1)
    return y3 - y1 == slope * (x3 - x1)

#angle returning
def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]
def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else:

        return ang_deg

#main diagonal
shape = len(img),
i,j,x,y = 0,0,shape[0],shape[0]
im_diag = math.hypot(x - i, y - j)

x, y, w, h = cv2.boundingRect(cnt)

#check if a dot from a diagonal found lies on main diagonal
iol = is_on_line(0,0,x,y, shape[0],shape[0])

if iol == True:
    if diag[1] == DISTANCE:
        print('Everything is fine, leap ahead.')
        coef = 1
    else:
        coef = DISTANCE / diag[1]
        print('The coefficient is set to %d.' % coef)
else:
    lin1 = np.asarray([(0, 0), (shape[0], shape[0])])
    lin2 = np.asarray([(x, y),(w, h)])
    angle = ang(lin1,lin2)
    rows, cols, dims = img.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img = cv2.warpAffine(img, M, (cols, rows))
    print('The image was rotated to %d degrees.' % angle)
    if diag[1] == DISTANCE:
        print('Everything is fine, leap ahead.')
        coef = 1
    else:
        coef = DISTANCE / diag[1]
        print('The coefficient is set to %d.' % coef)

print(img[x,y])

# if any(img[x,y]) < 20:
#     iol = is_on_line(0, 0, x, y, shape[0], shape[0])
#     if iol == False:
#         x = y
#         print(img[x,y])
#         if any(img[x,y]) <10:
#             print('Some mistake occured, the result is gonna be a mess.')
#         else:
#             print('Your zero x is %d' % x)
#             print('Your zero y is %d' % y)
#     else:
#         print('Everything is fine.')
# else:
#     print('Some mistake occured.')

masque_sh = img.shape[0],img.shape[1]
print(masque_sh)
#draw the mask
#shape area recognition, mask creation:
white = np.zeros((masque_sh), np.uint8)
cyan = np.zeros((masque_sh), np.uint8)
magenta = np.zeros((masque_sh), np.uint8)
yellow = np.zeros((masque_sh), np.uint8)
ROI = np.zeros((masque_sh), np.uint8)

#new constants of the shape pattern
BORDER = int(20*coef) # width of the borders
SQUARE = int(100*coef) #side of the white square
COLOR = int(40*coef) #side of CMY rectangle
ROI_side = int(160*coef) #side of ROI

# #smaller constants
# BORDER = 19*coef # width of the borders
# SQUARE = 99*coef #side of the white square
# COLOR = 39*coef #side of CMY rectangle
# ROI_side = 159*coef #side of ROI

print(x,y)

c=0
while c<4:
    ZERO_X=x
    #ZERO_X = x+1*coef
    ZERO_Y=y
    #ZERO_Y = y+1*coef
    cv2.rectangle(white, (ZERO_X,ZERO_Y), (ZERO_X+SQUARE,ZERO_Y+SQUARE), (255, 255, 255), -1)
    cy = ZERO_X+SQUARE+BORDER
    cv2.rectangle(cyan, (cy,ZERO_Y), (cy+COLOR,ZERO_Y+SQUARE), (255, 255, 255), -1)
    ye = cy+COLOR+BORDER
    cv2.rectangle(yellow, (ye,ZERO_Y), (ye + COLOR, ZERO_Y + SQUARE), (255, 255, 255), -1)
    ma =ye+COLOR+BORDER
    cv2.rectangle(magenta, (ma,ZERO_Y), (ma+COLOR, ZERO_Y + SQUARE), (255, 255, 255), -1)
    cv2.rectangle(ROI, (cy, cy), (cy+ROI_side, cy+ROI_side), (255, 255, 255), -1)
    #doublecheck
    cv2.rectangle(img, (ZERO_X, ZERO_Y), (ZERO_X + SQUARE, ZERO_Y + SQUARE), (0, 255, 0), 5)
    cv2.rectangle(img, (cy, ZERO_Y), (cy + COLOR, ZERO_Y + SQUARE), (0, 255, 0), 5)
    cv2.rectangle(img, (ye, ZERO_Y), (ye + COLOR, ZERO_Y + SQUARE), (0, 255, 0), 5)
    cv2.rectangle(img, (ma, ZERO_Y), (ma + COLOR, ZERO_Y + SQUARE), (0, 255, 0), 5)
    cv2.rectangle(img, (cy, cy), (cy + ROI_side, cy + ROI_side), (0, 255, 0), 5)
    cols, rows, dims = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    white = cv2.warpAffine(white,M,(cols,rows))
    cyan = cv2.warpAffine(cyan, M, (cols, rows))
    magenta = cv2.warpAffine(magenta, M, (cols, rows))
    yellow = cv2.warpAffine(yellow, M, (cols, rows))
    ROI = cv2.warpAffine(ROI, M, (cols, rows))
    # img = cv2.warpAffine(img, M, (cols, rows))
    c+=1


x,y,w,h = cv2.boundingRect(cnt)
cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

#get the colours
def get_average_color(masque, image):
    """ Returns a 3-tuple containing the RGB value of the average color of the
    given square bounded area of length = n whose origin (top left corner)
    is (x, y) in the given image"""

    r, g, b = 0, 0, 0
    count = 0
    for index, pixel in np.ndenumerate(masque):
        if pixel == 0:
            pass
        else:
            s,t = index
            pixlb, pixlg, pixlr = image[s,t]
            if pixlb == pixlg == pixlr == 0:
                pass
            else:
                b += pixlb
                g += pixlg
                r += pixlr
                count += 1
    return ((r / count), (g / count), (b / count))

avg_w = get_average_color(white,img)
avg_c = get_average_color(cyan,img)
avg_m = get_average_color(magenta,img)
avg_y = get_average_color(yellow,img)
avg_ROI = get_average_color(ROI, img)

#estimation of white balance
whites = []
blue = float(avg_w[0])
green = float(avg_w[1])
red = float(avg_w[2])

whites.append(float(blue/green))
whites.append(float(green/red))
whites.append(float(red/blue))
print(whites)

white_avg = (sum(avg_w))/len(avg_w)
print(avg_w)
print(white_avg)
white_per_cent = (white_avg/255)*100
print("White on the picture is %d per cent white." % white_per_cent)

#estimation of other colours averages
avgs = []

avgs.append((avg_c[2]+white_avg+avg_c[0]+avg_c[1])/len(avg_c)) #cyan
avgs.append((avg_y[0]+white_avg+avg_y[1]+avg_y[2])/len(avg_y)) #yellow
avgs.append((avg_m[1]+white_avg+avg_m[0]+avg_m[2])/len(avg_m)) #magenta
avgs.append(white_avg) #white

avgs_a = np.array([avgs])
print(avgs)
st_dev = np.std(avgs_a, ddof=1)
print(st_dev)

if st_dev>1.5:
    print("Your picture is not balanced.")
else:
    print("Your picture is well balanced.")'''

#cv2.rectangle(img, (int(x), int(y)), (w, h), (0, 255, 0), 5)
cv2.imshow("Mask", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
