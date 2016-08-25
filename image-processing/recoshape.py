#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import the necessary packages
import numpy as np
import cv2
import math
import argparse
from matplotlib import pyplot as plt
import matplotlib.mlab as mlab
from scipy.signal import argrelextrema
from scipy.stats import norm
import sys
import json


def pattern_pars(parameters_json):
    """
    Load the .json file that contains information on parameters of the shape for the analysis

    :param parameters_json: is a .json file either chosen by default from the repository or defined by the user
    :return:
    *_const are lists with x and y coordinates of the top left and bottom right of the rectangles
    tolerance is a float, a value that is used to select the ROI
    side is an int, length of a side of ROI
    """
    with open(parameters_json, 'r') as fp:
        param = json.load(fp)
    w_const = param['white_c']
    c_const = param['cyan_c']
    m_const = param['magenta_c']
    y_const = param['yellow_c']
    tolerance = param['tolerance']
    side = param['side']

    return w_const, c_const, m_const, y_const, tolerance, side


def show_pic(image_to_show, number_of_the_image):
    if args['panic']:
        cv2.imshow('analysis', image_to_show)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        name = os.path.join(args['panic'], 'pic'+number_of_the_image+'.jpg')
        cv2.imwrite(name, img)


def contours_selection_threshold(image):
    """
    Take an image for analysis, de-noise it by blurring and then threshold it to select the ROI with the pattern.

    :param image: a numpy 3-dimensional array, that is an image loaded with cv2
    :return:
    :cnts: list, contours found
    :tresh: numpy 3-dimensional array, a thresholded image
    """

    image = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret2, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    tresh = np.copy(th2)
    im, cnts, hier = cv2.findContours(th2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    return cnts, tresh


def square_selection(contours, image, tol):
    """
    Select the contour of the ROI of a pattern.

    :type contours: list, all of the contours found in the image
    :type image: np.ndarray, the original image
    :type tol: float, most part of the image
    :return:
    sq: float, area of ROI
    """
    areas = []
    height = int(image.shape[0])
    width = int(image.shape[1])
    for contour in contours:
        areas.append(cv2.contourArea(contour))
    c_areas = np.asarray(areas)

    # The biggest areas are the whole image and a square
    top = c_areas.argsort()[-2:][::-1]
    c = cv2.contourArea(contours[top[0]])

    if c >= tol * height * width:
        print('The biggest contour is the picture border, the second biggest contour was selected.')
        sq = int(top[1])
    else:
        print('The biggest contour is not defined properly. The result might be unreliable.')
        sq = int(top[0])

    return sq


def square_or_not(sq_contour):
    """
    Check, whether the found contour is a square.

    :type sq_contour: list, coordinates of the contour selected as a ROI
    :return:
    :approx: list of coords, approximation of the contour,
    :type square_log: bool
    """
    perimeter = cv2.arcLength(square_contour, True)
    if perimeter == 0:
        print('The square is not recognized.')
    else:
        epsilon = 0.1 * perimeter
        approx = cv2.approxPolyDP(square_contour, epsilon, True)
        if len(approx) > 4:
            print('The square is not recognized.')
        if len(approx) == 2:
            print("It is a square!")
            square_log = True
        else:
            square_log = False
        return approx, square_log


def coords_check(approx, square_log):
    """
    Select the coordinates of the ROI according to the approximation

    :type approx: list, coordinates of an approximated contour
    :type square_log: bool, statement whether the ROI is square
    :return: coordinates of the ROI rectangle
    """
    if square_log:
        x, z = approx
        x = x[0]
        y = (0, 0)
        z = z[0]
        h = (0, 0)
    else:
        x, y, z, h = approx
        x = tuple(x[0])
        y = tuple(y[0])
        z = tuple(z[0])
        h = tuple(h[0])
    return x, y, z, h


def draw_the_sq(approx_contour, component, mask, square_log):
    x, y, z, h = coords_check(approx_contour, square_log)
    cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
    component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
    cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    c = 0
    for (l, m), unit in np.ndenumerate(component):
        if component[l, m] == mask[l, m]:
            c += 0
        else:
            c += 1

    # checkpoint marker tells whether the square is distorted,
    # might be combined with distortion-correction algorithm

    if c > image.shape[0] * image.shape[1] * tol:
        print('Your square fits perfectly.')
        checkpoint = True
    else:
        print('The square is rotated or distorted.')
        checkpoint = False

    return mask, checkpoint_log, square_log


def draw_the_stuff(approx_contour, component, mask, square_log):
    x, y, z, h = coords_check(approx_contour, square_log)
    cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
    cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
    component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    print('There are new coordinates of corners lying inside the contour of the square.')
    if mask[x[1], x[0]] == 255:
        print('Your square fits perfectly.')
        checkpoint_log = True
    else:
        print('The square is rotated or distorted.')
        checkpoint_log = False
    return mask, checkpoint_log, square_log

def shrink_the_mask(square_contour, image, sq_log):
    component = np.zeros_like(image)
    mask = np.zeros_like(image)
    if len(approx) == 2:
        mask, chp_log, sq_log = draw_the_sq(approx, component, mask, sq_log)
    else:
        mask, chp_log, sq_log = draw_the_stuff(approx, component, mask, sq_log)

    return approx, mask, component, sq_log, chp_log


def geometry_of_white(image, list_of_corners, width, height, constants):
    # this finds white areas
    # constants are known from the palette sketch found in sample folder
    x_coef = width / side
    y_coef = height / side
    wi = constants[0]
    he = constants[1]
    # d_coef = diag / 678.8225099390856

    white = np.zeros_like(image)
    white_coords = []

    for i in list_of_corners:
        if i[0] < centre[0]:
            x = int(i[0] + wi * x_coef)
            p = int(i[0] + he * x_coef)
            if i[1] < centre[1]:
                y = int(i[1] + wi * y_coef)
                q = int(i[1] + he * y_coef)
            else:
                y = int(i[1] - wi * y_coef)
                q = int(i[1] - he * y_coef)
        else:
            x = int(i[0] - wi * x_coef)
            p = int(i[0] - he * x_coef)
            if i[1] < centre[1]:
                y = int(i[1] + wi * y_coef)
                q = int(i[1] + he * y_coef)
            else:
                y = int(i[1] - wi * y_coef)
                q = int(i[1] - he * y_coef)

        white_coords.append(((x, y), (p, q)))

    # white can be seen if "panic regime" is on
    for i in white_coords:
        cv2.rectangle(white, i[0], i[1], (255, 255, 255), -1)

    pts = np.where(white == [255, 255, 255])

    x = pts[0]
    y = pts[1]

    wh = []
    for i in range(len(x)):
        wh.append((x[i], y[i]))

    intensities = []
    for i in range(len(wh)):
        x, y = wh[i]
        intensities.append(image[x, y])
        white[x, y] = intensities[i]

    whites = np.unique(white)
    whites = whites[1:]

    return whites, intensities, white


def geometry_of_color(image, list_of_corners, width, height, constants):
    # this finds white areas
    # constants are known from the palette sketch found in sample folder
    x_coef = width / 480
    y_coef = height / 480
    wi1 = constants[0]
    wi2 = constants[1]
    he1 = constants[2]
    he2 = constants[3]
    # d_coef = diag / 678.8225099390856

    color = np.zeros_like(image)
    color_coords = []

    for i in list_of_corners:
        if i[0] < centre[0]:
            if i[1] < centre[1]:
                x = int(i[0] + wi1 * x_coef)
                p = int(i[0] + wi2 * x_coef)
                y = int(i[1] + he1 * y_coef)
                q = int(i[1] + he2 * y_coef)
            else:
                x = int(i[0] + he1 * x_coef)
                p = int(i[0] + he2 * x_coef)
                y = int(i[1] - wi1 * y_coef)
                q = int(i[1] - wi2 * y_coef)
        else:
            if i[1] < centre[1]:
                x = int(i[0] - he1 * x_coef)
                p = int(i[0] - he2 * x_coef)
                y = int(i[1] + wi1 * y_coef)
                q = int(i[1] + wi2 * y_coef)
            else:
                x = int(i[0] - wi1 * x_coef)
                p = int(i[0] - wi2 * x_coef)
                y = int(i[1] - he1 * y_coef)
                q = int(i[1] - he2 * y_coef)

        color_coords.append(((x, y), (p, q)))

    # white can be seen if "panic regime" is on
    for i in color_coords:
        cv2.rectangle(color, i[0], i[1], (255, 255, 255), -1)

    pts = np.where(color == [255, 255, 255])

    x = pts[0]
    y = pts[1]

    col = []
    for i in range(len(x)):
        col.append((x[i], y[i]))

    intensities = []
    for i in range(len(col)):
        x, y = col[i]
        intensities.append(image[x, y])
        color[x, y] = intensities[i]

    return intensities, color


def whitecheck(white_pixel_values):
    white_av = sum(white_pixel_values) / (len(white_pixel_values))
    for i in range(len(white_pixel_values)):
        a = round(white_pixel_values[i] / white_av)
        c = 0
        if a != 1:
            c += 1

    if c > 0:
        print("White areas are not recognized.")
    else:
        print("White is white. Let it be.")

    color_dev = np.std(white_pixel_values)
    print(white_pixel_values)
    print("Colors may vary in range +/- %d in each channel" % color_dev)

    return white_av, color_dev


def color_average(values_interval):
    # values interval is a list of pixel values
    r, g, b = 0, 0, 0
    count = 0
    for i, c in enumerate(values_interval):
        pixlb, pixlg, pixlr = c
        r += pixlr
        g += pixlg
        b += pixlb
        count += 1
    return (r / count), (g / count), (b / count)


def info(array):
    a = type(array)
    b = array[0]
    c = array.shape

    return a, b, c


# Construct the argument parse and parse the arguments
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='let the process begin')
    ap.add_argument('-i', '--image', required=True, help='Full path to the image')
    ap.add_argument('-p', '--panic', help='Show every image on each step and save it to the directory mentioned')
    ap.add_argument('-j', '--json',
                    help='Path to the json parameters file with the constants required for the analysis',
                    default='const.json')
    args = vars(ap.parse_args())

    w_const, c_const, m_const, y_const, tolerance, side = pattern_pars(args['json'])
    img = cv2.imread(args['image'])
    contours, th2 = contours_selection_threshold(img)
    top = square_selection(contours, img, tolerance)

    # Checkpoint of contour sides
    approx, square_log = square_or_not(contours[sq])
    topleft, botleft, botright, topright = coords_check(approx, square_log)
    , mask, component, square, checkpoint = shrink_the_mask(contours[sq], img)

    if square:
        botleft = (topleft[0], botright[1])
        topright = (botright[0], topleft[1])
        corners = [topleft, botleft, botright, topright]
    else:
        corners = [topleft, botleft, botright, topright]

    # Getting the centre of the contour
    moments = cv2.moments(contours[sq])
    centre = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))

    diag = math.hypot(float(topleft[0]) - float(botright[0]), float(topleft[1]) - float(botright[1]))
    wid = math.hypot(float(topleft[0]) - float(topright[0]), float(topleft[1]) - float(topright[1]))
    hei = math.hypot(float(topleft[0]) - float(botleft[0]), float(topleft[1]) - float(botleft[1]))

    if diag ** 2 == wid ** 2 + hei ** 2:
        print('Everything is fine.')

    print('The diagonal of the rectangle is %d.' % diag)
    print('The width of the rectangle is %d.' % wid)
    print('The height of the rectangle is %d.' % hei)

    whites, intensities, white = geometry_of_white(img, corners, wid, hei, w_const)

    white_av, color_dev = whitecheck(whites)

    cy_int, cyan = geometry_of_color(img, corners, wid, hei, c_const)

    show_pic(cyan)

    ma_int, magenta = geometry_of_color(img, corners, wid, hei, m_const)

    show_pic(magenta)

    ye_int, yellow = geometry_of_color(img, corners, wid, hei, y_const)

    show_pic(yellow)

    # Comparing the retreived values

    cy_r, cy_g, cy_b = color_average(cy_int)
    ma_r, ma_g, ma_b = color_average(ma_int)
    ye_r, ye_g, ye_b = color_average(ye_int)

    print(cy_r, cy_g, cy_b, white_av)
    print(ma_r, ma_g, ma_b, white_av)
    print(ye_r, ye_g, ye_b, white_av)

    if cy_r < ma_r:
        if cy_r < ye_r:
            cyanred = True
        else:
            cyanred = False
    else:
        cyanred = False

    if ma_g < cy_g:
        if ma_g < ye_g:
            magentagreen = True
        else:
            magentagreen = False
    else:
        magentagreen = False

    if ye_b < cy_b:
        if ye_b < ma_b:
            yellowblue = True
        else:
            yellowblue = False
    else:
        yellowblue = False

    if cyanred:
        print("Your cyan is cyan")
    else:
        print("Your cyan is not quite cyan, normalisation is required.")

    if magentagreen:
        print("Your magenta is magenta")
    else:
        print("Your magenta is not quite magenta, normalisation is required.")

    if yellowblue:
        print("Your yellow is yellow")
    else:
        print("Your yellow is not quite yellow, normalisation is required.")

    # Normalisation of values
    show_pic(whites)
    # finding contour areas

print("the end")
