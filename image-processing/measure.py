import math
import matplotlib.pyplot as plt
import numpy as np
from skimage import feature, color
from PIL import Image
from skimage.measure import label, regionprops


# Import a test image, preprocessing
im = Image.open("/Users/apple/tutorial/test.jpg")
im = np.asarray(im)
gimg = color.rgb2gray(im)
print('You are now working with', type(gimg))

# Compute the Canny filter for two values of sigma
# In this code -- sigma1 = 1, sigma2 = 1.8
edges1 = feature.canny(gimg)
print(type(edges1))
print(len(edges1))

label_img = label(edges1)
print(type(label_img))
print(len(label_img))
regions = regionprops(label_img)
print(type(regions))
print(len(regions))


'''fig, ax = plt.subplots()
ax.imshow(regions, cmap=plt.cm.gray)

for props in regions:
    y0, x0 = props.centroid
    orientation = props.orientation
    x1 = x0 + math.cos(orientation) * 0.5 * props.major_axis_length
    y1 = y0 - math.sin(orientation) * 0.5 * props.major_axis_length
    x2 = x0 - math.sin(orientation) * 0.5 * props.minor_axis_length
    y2 = y0 - math.cos(orientation) * 0.5 * props.minor_axis_length

    ax.plot((x0, x1), (y0, y1), '-r', linewidth=2.5)
    ax.plot((x0, x2), (y0, y2), '-r', linewidth=2.5)
    ax.plot(x0, y0, '.g', markersize=15)

    minr, minc, maxr, maxc = props.bbox
    bx = (minc, maxc, maxc, minc, minc)
    by = (minr, minr, maxr, maxr, minr)
    ax.plot(bx, by, '-b', linewidth=2.5)

ax.axis((0, 600, 600, 0))
plt.show()'''