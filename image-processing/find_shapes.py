import numpy as np
import matplotlib.pyplot as plt
from skimage import feature, color
from PIL import Image

# Import a test image, preprocessing
im = Image.open("/Users/apple/tutorial/test.jpg")
im = np.asarray(im)
gimg = color.rgb2gray(im)
print('You are now working with', type(gimg))

# Compute the Canny filter for sigma = 1
edges1 = feature.canny(gimg)
print(type(edges1))
print(len(edges1))
print(edges1)

# Select ROI
