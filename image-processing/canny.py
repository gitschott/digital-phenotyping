import numpy as np
import matplotlib.pyplot as plt
from skimage import feature, color
from PIL import Image

# Import a test image, preprocessing
im = Image.open("/Users/apple/tutorial/test.jpg")
im = np.asarray(im)
gimg = color.rgb2gray(im)
print('You are now working with', type(gimg))

# Compute the Canny filter for two values of sigma
# In this code -- sigma1 = 1, sigma2 = 1.8
edges1 = feature.canny(gimg)
edges2 = feature.canny(gimg, sigma=1.8)

# Display results
fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3),
                                    sharex=True, sharey=True)

ax1.imshow(gimg, cmap=plt.cm.gray)
ax1.axis('off')
ax1.set_title('Image to analyze', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title('Canny filter, $\sigma=1.8$', fontsize=20)

fig.tight_layout()

plt.show()