##The folder contains current progress on image processing branch. 

Here one can find:
* comparison of image processing algorithms,
* examples (images),
* algorithms themselves.

##How to select a ROI for analysis?
Main idea is to highlight the borders and then to analyze properties within the borders. Possible packages to be used are:
* OpenCV (CV stands for Computer Vision),
* Scikit-image.

###OpenCV
OpenCV requires XCode to be downloaded on the PC (for OSX). Due to obstacles with the internet connection, it was impossible to download XCode today. I shall fix it by getting Thunderbolt Mac adapter.

###Scikit-image
Scikit image allows several processing options for image analysis, they are:
1. Canny edge detector.
2. Local Otsu threshold.
3. Felzenszwalb’s efficient graph based segmentation.
4. Quickshift image segmentation.
5. SLIC - K-Means based image segmentation.

Scikit also has a module for inter-segment values analysis.

##Algorithm test.
For test image a photo with RGB circles was selected, called test.jpg. There was an idea to use this image as a reference table and to cut a slit in the middle of it so that the skin sample won't be affected either by shadow or by light (in case of light-affected shift all of the color values will be shifted).

Brief descriptions of the algorithms are provided below. Only main differences are highlighted. 
Canny and Local Otsu require 2D array, that is why the image was converted to grayscale.  

### Canny edge detector.
The Canny filters an image through multiple stages of Gaussian-like filtering. It estimates intensity of the gradients. Gaussian algorithm reduces the noise, then non-maximum pixels are removed of the gradient magnitude. Finally, potential edges are shrieked to one-pixel curves. (I am not sure I understand what is hysteresis thresholding, but it is also used here).
Parameters:
* the width of the Gaussian (the noisier the image, the greater the width),
* low threshold,
* high threshold (for the hysteresis thresholding).
Examples are pushed in the repo: example_canny*.png,
Script: canny.py

Source: skimage 0.13dev

###Local Otsu threshold
This algorithm thresholds each pixel of an image according to an «optimal threshold». «OT» is a maximized variance between two classes of pixels in the local neighborhood, which are somehow «defined by a structuring element» (the latter phrase looks puzzling to me).
Limitations (according to the ref on Wiki):
* small object size,
* small mean difference,
* large variances of object / background intensities,
* large amount of noise,
* etc.

Examples are pushed in the repo: example_otsu*.png,
Script: otsu.py

Source: ==

###Comparison of segmentation algorithms.
Felzenszwalb’s is a fast 2D image segmentation algorithm. Size and number of segments can vary greatly, depending on local contrast.
Parameter:
* scale (size of segments).

Source: Felzenszwalb, Pedro F., and Daniel P. Huttenlocher. "Efficient graph-based image segmentation." International Journal of Computer Vision 59.2 (2004): 167-181.

Honestly speaking, I am not that acquainted with the parameters yet. 
