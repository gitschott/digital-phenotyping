from PIL import Image
import PIL.ImageOps

image1 = Image.open('/Users/apple/tutorial/square1.jpg')
image2 = Image.open('/Users/apple/tutorial/square2.jpg')

inverted_image1 = PIL.ImageOps.invert(image1)
inverted_image2 = PIL.ImageOps.invert(image2)

inverted_image1.save('erauqs1.jpg')
inverted_image2.save('erauqs2.jpg')