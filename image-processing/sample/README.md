##Content

This directory contains a script that creates a coloured pattern. The pattern is built on prescribed in the piece_parameters.json. The pattern is saved as piece.jpg in the directory set by user.
To create a coloured shape:

    python3 five_sliced_shape.py -p full/path/to/parameters.json -s path/to/the/pattern/to/save/

The script takes 2 arguments:

 -p or --parameters defines which json parameter file to use. The json parameter file contains the following information on the shape:
* the width of the border between coloured rectangles and the edge of the square
* the width of each coloured (C, M or Y) rectangle
* size of the white square side
* starting points (x and y, which are sq_height and sq_width, respectively)
* total size of the picture, the coordinates of the bottom right corner (total_height and total_width)
One can create his own json parameters file for the pattern.

-s or --save defines the path to the pattern. It is a required argument.
