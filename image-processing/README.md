#Contents.
1. Introduction.
2. Problem description.
3. Solution. Brief tool description.
4. Further steps.

##Introduction
Phenotype prediction in silico implies usage of standard formally defined phenotypes and their classification. Primary goal is creation of skin pigmentation recognition tool that can measure an average of skin colour tone. Average skin colour tone can be meaningful and representative for a colour tone of an individual [1].

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

Current version allows:
* Palette pattern recognition (to be tested)
* Average pixel values estimation (to be tested)

## Further steps

1. Colour analysis debugging.
2. Geometrical test / correction / evaluation of CMYK reference regions.
3. Testing of real photos.
4. Recognition tests and recognizing classifyer.
5. White balance correction.
6. Skin tone classifier.

##References
1. Candille S. I. et al. Genome-wide association studies of quantitatively measured skin, hair, and eye pigmentation in four European populations //PLoS One. – 2012. 
