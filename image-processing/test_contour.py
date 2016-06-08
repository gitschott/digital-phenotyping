import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage import measure


# Open an image
im = Image.open("/Users/apple/tutorial/set/tumblr_o72jmrfSkl1rvapjbo1_500.jpg")
print(type(im))
pic = np.asarray(im)
print(type(pic))


# Find contours at a constant value of 0.8
contours = measure.find_contours(pic, 0.8)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(pic, interpolation='nearest', cmap=plt.cm.gray)

for n, contour in enumerate(contours):
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()