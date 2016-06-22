#Contents.
1. Introduction.
2. Problem description.
3. Solution. Brief tool description.
4. Images for analysis.
5. Further steps.

##Introduction
Phenotype prediction in silico implies usage of standard formally defined phenotypes and their classification. Primary goal is creation of skin pigmentation recognition tool that can measure an average of skin colour tone. Average skin colour tone can be meaningful and representative for a colour tone of an individual [1](Candille S. I. et al. Genome-wide association studies of quantitatively measured skin, hair, and eye pigmentation in four European populations //PLoS One. – 2012).

Here, an algorithm of skin color analysis is presented.

##Problem description
Skin pigmentation instant photo analysis is a subtle matter. The main problem in the analysis of regular photos is white balance and coping with overlighted regions. It is crucial for skin analysis, since skin is a plain-coloured matter on the one hand and highly variable on the other. There are several issues that can be used to make the analysis more neat and simple:

1. To use the HSV colour mode rather than RGB. It allows ignoring of the lightness, thus, allows less normalization steps.
2. To take a photo with a color standart. In this case a CMYK palette was used, as it allows calibration upon pure solid colors.
3. Border area has to be wide, as it allows better recognition and processsing.
4. The palette has to be symmetrical and small.

## Brief tool description.

This is a tool for skin color recognition and analysis. 

There is a small rigid coloured frame which is a CMYK palette that is to be put on the skin and photographed. There is an opening inside that frame in the middle. It shows the skin sample that is analyzed further. 

The photo then is uploded as an argument to recognize.py and processed. First step is contour selection. Second step is mask creation. Next step is retrieval and averaging of color values.

The algorithm requires OpenCV library to be pre-installed. Comprehensive OpenCV installation tutorial is availiable [2](http://docs.opencv.org/2.4/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html "OpenCV installation Tutorials"). 

Current version allows:
* Palette pattern recognition (to be tested)
* Average pixel values estimation (to be tested)

##Images for analysis

1) Image has to have RGB profile.
2) The CMYK frame has to be put on the plain skin sample without spots, ink marks or tattoos.
3) The CMYK frame contours have to be the darkest part of the image (the background has to be light, no big black or very dark objects have to be on the photo).
4) The CMYK palette has to be installed on the sample with no wrinkles and no heavy shadows.

Current dataset:
5409.jpg, 54055.jpg failed the test.

## Further steps

1. Colour analysis debugging.
2. Geometrical test / correction / evaluation of CMYK reference regions.
3. Testing of real photos.
4. Recognition tests and recognizing classifyer.
5. White balance correction.
6. Skin tone classifier.

