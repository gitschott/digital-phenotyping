import numpy as np
from skimage import feature, color
from PIL import Image
from matplotlib import pyplot as plt
from scipy import ndimage
from skimage.transform import ( probabilistic_hough_line)

''' Import a test image, preprocessing
img = Image.open("/Users/apple/tutorial/square2.jpg")
img2 = Image.open("/Users/apple/tutorial/erauqs2.jpg")
img = np.asarray(img)
img2 = np.asarray(img2)
im = color.rgb2gray(img)
im2 = color.rgb2gray(img2)

find lines Sobel
sx = ndimage.sobel(im, axis=0, mode='constant')
sy = ndimage.sobel(im, axis=1, mode='constant')
sob = np.hypot(sx, sy)
sx2 = ndimage.sobel(im2, axis=0, mode='constant')
sy2 = ndimage.sobel(im2, axis=1, mode='constant')
sob2 = np.hypot(sx2, sy2)

#stats
print(type(sob))
print(len(sob))
print(sob.shape)
print(sob.ndim)
print(sob)

#pic = plt.imshow(sob)
#plt.show()'''

# Import a test image, preprocessing
im = Image.open("/Users/apple/tutorial/square2.jpg")
im = np.asarray(im)
img = color.rgb2gray(im)
print('You are now working with', type(img))

# Compute the Canny filter
edges = feature.canny(img)

# Line finding, using the Probabilistic Hough Transform

lines = probabilistic_hough_line(edges, threshold=10, line_length=5,
                                 line_gap=3)

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 4), sharex=True, sharey=True)

ax1.imshow(img, cmap=plt.cm.gray)
ax1.set_title('Input image')
ax1.set_axis_off()
ax1.set_adjustable('box-forced')

ax2.imshow(edges, cmap=plt.cm.gray)
ax2.set_title('Sob')
ax2.set_axis_off()
ax2.set_adjustable('box-forced')

ax3.imshow(edges * 0)
for line in lines:
    p0, p1 = line
    ax3.plot((p0[0], p1[0]), (p0[1], p1[1]))

ax3.set_title('Probabilistic Hough')
ax3.set_axis_off()
ax3.set_adjustable('box-forced')
plt.show()


'''#values
maximum = np.amax(sob)
minimum = np.amin(sob)
max = sob
max[max<(maximum-1)]=0
print(max)
min = sob
min[min>(minimum+1)]=3

fig, (plt1, plt2) = plt.subplots(nrows=1, ncols=2, sharex=False, sharey=False)

plt1.imshow(max)
plt1.axis('off')

plt2.imshow(min)
plt2.axis('off')

#fig.tight_layout()
#plt.show()
'''

'''Display results
fig, (plt1, plt2, plt3, plt4) = plt.subplots(nrows=1, ncols=4, figsize=(10, 3),
                                             sharex=True, sharey=True)

plt1.imshow(sob)
plt1.axis('off')
plt1.set_title('Sob result', fontsize=20)

plt2.imshow(sob2)
plt2.axis('off')
plt2.set_title('Sob result', fontsize=20)

plt3.imshow(img)
plt3.axis('off')
plt3.set_title('Sample1', fontsize=20)

plt4.imshow(img2)
plt4.axis('off')
plt4.set_title('Sample2', fontsize=20)

fig.tight_layout()

plt.show()'''