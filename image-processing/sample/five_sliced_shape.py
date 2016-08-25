import numpy as np
import cv2
import json
import argparse
import os

def pattern_pars(parameters_dict):
    # load parameters of shapes:
    with open(parameters_dict, 'r') as fp:
        frame = json.load(fp)
    border = frame["border"] # width of the borders
    shape_height = frame["sq"] # side of the white square
    rect_width = frame["color"] # side of CMY rectangle
    x = frame["sq"] # starting coordinate x
    y = frame["sq"] # starting coordinate y
    cyan = x + shape_height + border
    yellow = cyan + rect_width + border
    magenta = yellow + rect_width + border
    t_height = frame["total_height"]
    t_width = frame["total_width"]

    return border, shape_height, rect_width, x, y, cyan, yellow, magenta, t_height, t_width

def color_coords(x, y, rect_width, rect_height):
    # input is the starting coords of a coloured rectangle and the width + height
    end = (x + rect_width, y + rect_height)

    return end


def side_drawer(border, sq, color, x, y, cyan, yellow, magenta, t_height, t_width):
    cv2.rectangle(img, (x, y), color_coords(x, y, sq, sq), (255, 255, 255), -1)
    cv2.rectangle(img, (cyan, y), color_coords(cyan, y, color, sq), (255, 255, 0), -1)
    cv2.rectangle(img, (yellow, y), color_coords(yellow, y, color, sq), (0, 255, 255), -1)
    cv2.rectangle(img, (magenta, y), color_coords(magenta, y, color, sq), (255, 0, 255), -1)

    return img

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description="creating a basic shape")
    ap.add_argument("-p", "--parameters", help="Path to the shape parameters, "
                                               "default: piece_parameters.json",
                    default = "piece_parameters.json")
    ap.add_argument('-s', '--save', help="Path to the created pattern", required = True)
    args = vars(ap.parse_args())

    border, shape_height, rect_width, start_x, start_y, cyan, \
    yellow, magenta, t_height, t_width = pattern_pars('piece_parameters.json')

    c = 0
    # the shape is symmetrical and the pattern depends on the initial parameters above
    # when the first side is drawn the shape is rotated at 90 degrees and the next side is drawn in the same fashion
    img = np.zeros((t_height, t_width, 3), np.uint8)
    img[:] = (0, 0, 0)
    while c < 4:
        img = side_drawer(border, shape_height, rect_width, start_x, start_y, cyan, yellow, magenta, t_height, t_width)
        cols, rows, dims = img.shape
        M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 90, 1)
        img = cv2.warpAffine(img, M, (cols, rows))
        c += 1

    # Draw a white frame
    cv2.rectangle(img, (0, 0), (t_height, t_width), (255, 255, 255), 120)
    # Draw the ROI area
    cv2.rectangle(img, (cyan, cyan), (380,380), (255, 255, 255), -1)

    # Save
    name = os.path.join(args["save"], "piece.jpg")
    cv2.imwrite(name, img)
    # Display the image
    cv2.imshow("img", img)
    cv2.waitKey(0)