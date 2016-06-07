from __future__ import print_function
import re
import numpy as np
import pylab as plt
from PIL import Image
from skimage.segmentation import felzenszwalb, clear_border


# Open an image
im = Image.open("/Users/apple/tutorial/test.jpg")
print(type(im))
img = np.asarray(im)

segments_fz = felzenszwalb(img, scale=100, sigma=0.5, min_size=50)
print(type(segments_fz))
print(len(segments_fz))
print("Felzenszwalb's number of segments: %d" % len(np.unique(segments_fz)))

#segments_fz = clear_border(segments_fz)
print(type(segments_fz))
print(len(segments_fz))
print(segments_fz)


#middle = filter(lambda x:re.search(r'186', x), segments_fz)
a = segments_fz.shape
mid = (a[0] / 2, a[1] / 2)
print(mid)
light = segments_fz[mid]
print(light)

segmts = segments_fz
segmts[segmts!=light] = 0

print(type(segmts))
print(len(segmts))
print(segmts)

pic = plt.imshow(segmts)
plt.show()

'''fig, ax = plt.subplots(1, 3, sharex=True, sharey=True,
                       subplot_kw={'adjustable': 'box-forced'})
fig.set_size_inches(8, 3, forward=True)
fig.tight_layout()

ax[0].imshow(mark_boundaries(img, segments_fz))
ax[0].set_title("Felzenszwalbs's method")
ax[1].imshow(mark_boundaries(img, segments_slic))
ax[1].set_title("SLIC")
ax[2].imshow(mark_boundaries(img, segments_quick))
ax[2].set_title("Quickshift")
for a in ax:
    a.set_xticks(())
    a.set_yticks(())
plt.show()'''