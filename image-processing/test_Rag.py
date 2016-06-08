from skimage.future import graph
from skimage import data, segmentation, color, filters, io
from skimage.util.colormap import viridis
from PIL import Image
import numpy as np


# Open an image
im = Image.open("/Users/apple/tutorial/test.jpg")
print(type(im))
pic = np.asarray(im)
print(type(pic))
gimg = color.rgb2gray(pic)
#himg = color.rgb2hsv(pic)

labels = segmentation.slic(pic, compactness=30, n_segments=400)
edges = filters.sobel(gimg)
#edhes = filters.sobel(himg)
edges_rgb = color.gray2rgb(edges)
#edges_rgb_h = color.hsv2rgb(edges)

g = graph.rag_boundary(labels, edges)

out1 = graph.draw_rag(labels, g, edges_rgb, node_color="#999999",
                     colormap=viridis)
#out2 = graph.draw_rag(labels, g, edges_rgb_h, node_color="#999999", colormap=viridis)

io.imshow(out1)
io.show()