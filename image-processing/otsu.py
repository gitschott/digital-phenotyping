import matplotlib
import matplotlib.pyplot as plt
from skimage.morphology import disk
from skimage.filters import threshold_otsu, rank
from PIL import Image
import numpy as np
from skimage import color


matplotlib.rcParams['font.size'] = 9

# Import a test image, preprocessing
im = Image.open("/Users/apple/tutorial/test.jpg")
im = np.asarray(im)
img = color.rgb2gray(im)
print('You are now working with', type(img))

radius = 5
selem = disk(radius)

local_otsu = rank.otsu(img, selem)
threshold_global_otsu = threshold_otsu(img)
global_otsu = img >= threshold_global_otsu


fig, ax = plt.subplots(2, 2, figsize=(8, 5), sharex=True, sharey=True, subplot_kw={'adjustable':'box-forced'})
ax1, ax2, ax3, ax4 = ax.ravel()

fig.colorbar(ax1.imshow(img, cmap=plt.cm.gray),
             ax=ax1, orientation='horizontal')
ax1.set_title('Original')
ax1.axis('off')

fig.colorbar(ax2.imshow(local_otsu, cmap=plt.cm.gray),
             ax=ax2, orientation='horizontal')
ax2.set_title('Local Otsu (radius=%d)' % radius)
ax2.axis('off')

ax3.imshow(img >= local_otsu, cmap=plt.cm.gray)
ax3.set_title('Original >= Local Otsu' % threshold_global_otsu)
ax3.axis('off')

ax4.imshow(global_otsu, cmap=plt.cm.gray)
ax4.set_title('Global Otsu (threshold = %d)' % threshold_global_otsu)
ax4.axis('off')

plt.show()