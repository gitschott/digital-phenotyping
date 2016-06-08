from PIL import Image
im = Image.open('Documents/moments/personal/IMG_4396.JPG') #Can be many different formats.
pix = im.load(im)
print var = im.size  #Get the width and hight of the image for iterating over
print pixel = pix[600, 400]  #Get the RGBA Value of the a pixel of an image
pix[x,y] = value # Set the RGBA Value of the image (tuple)