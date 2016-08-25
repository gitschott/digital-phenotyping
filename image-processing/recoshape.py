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
import os


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
    w_const = param['w_const']
    c_const = param['c_const']
    m_const = param['m_const']
    y_const = param['y_const']
    tolerance = param['tol']
    side = param['side']

    return w_const, c_const, m_const, y_const, tolerance, side


def show_pic(image_to_show, number_of_the_image):
    if args['panic']:
        cv2.imshow('image_to_show', image_to_show)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        frag = str(number_of_the_image)
        name = os.path.join(args['panic'], 'pic'+frag+'.jpg')
        cv2.imwrite(name, img)
        number_of_the_image +=1
        return number_of_the_image


def contours_selection_threshold(image):
    """
    Take an image for analysis, de-noise it by blurring and then threshold it to select the ROI with the pattern.

    :param image: image loaded with cv2
    :type image: np.ndarray
    :return:
    :type cnts: list
    :cnts: contours found
    :type tresh: np.ndarray
    :tresh: thresholded image
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

    :param contours: all of the contours found in the image
    :type contours: list
    :param image: the original image
    :type image: np.ndarray
    :param tol: most part of the image
    :type tol: float
    :return:
    sq: the selected contour
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

    sq = contours[sq]
    return sq


def square_or_not(sq_contour):
    """
    Check, whether the found contour is a square.

    :type sq_contour: list, coordinates of the contour selected as a ROI
    :type approx: list
    :return approx: approximation of the contour coordinates
    :type square_log: bool
    :return square_log: the found contour is a square
    """
    perimeter = cv2.arcLength(sq_contour, True)
    if perimeter == 0:
        print('The square is not recognized.')
    else:
        epsilon = 0.1 * perimeter
        approx = cv2.approxPolyDP(sq_contour, epsilon, True)
        # if the list has more than 4 elements, the contour is not rectangular
        # if the list has just 2 elements, these are the square coordinates
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


def count_match(array1, array2):
    """
    Count matches between two arrays.

    :type array1: np.ndarray
    :param array2: np.ndarray
    :return: int, counts
    """
    c = 0
    for (l, m), unit in np.ndenumerate(array1):
        if array1[l, m] == array2[l, m]:
            c += 0
        else:
            c += 1
    return c


def chpoint_check(image, mask, component, sq_log, x, tolerance):
    """
    Check is square distorted or not, might be combined with distortion-correction algorithm

    :type image: np.ndarray, original image
    :type mask: np.ndarray, size of original image
    :type component: np.ndarray, size of original image
    :type sq_log: bool, tells whether the found ROI is a square
    :type x: tuple, coordinates of the top left corner
    :return:
    :type checkpoint_log: bool, True if the mask is square, False if distortions are found
    """
    if sq_log:
        counts = count_match(component, mask)
        if counts > image.shape[0] * image.shape[1] * tolerance:
            print('Your square fits perfectly.')
            checkpoint_log = True
        else:
            print('The square is rotated or distorted.')
            checkpoint_log = False
    else:
        print('There are new coordinates of corners lying inside the contour of the square.')
        if mask[x[1], x[0]] == 255:
            print('Your square fits perfectly.')
            checkpoint_log = True
        else:
            print('The square is rotated or distorted.')
            checkpoint_log = False
    return checkpoint_log


def draw_the_sq(approx_contour, square_contour, mask, component, square_log):
    """
    When the mask is recognised as a square, it is to be drawn.

    :type approx_contour: list, approximated contour coordinates
    :type square_contour:
    :type component: np.ndarray, size of original image
    :type mask: np.ndarray, size of original image
    :type square_log: bool, tells whether the found ROI is a square
    :return:
    :type mask: np.ndarray,
    :type component:
    :type checkpoint_log:
    """
    x, y, z, h = coords_check(approx_contour, square_log)
    cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
    component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
    cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    return mask, component


def draw_the_stuff(approx_contour, square_contour, mask, component, square_log):
    """

    :param approx_contour:
    :param square_contour:
    :param mask:
    :param component:
    :param square_log:
    :param tolerance:
    :return:
    """
    x, y, z, h = coords_check(approx_contour, square_log)
    cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
    cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
    component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    return mask, component


def shrink_the_mask(approx, square_contour, image, sq_log, tolerance):
    """

    :type approx_contour: list, approximated contour coordinates
    :param square_contour:
    :param image:
    :param sq_log:
    :param tolerance:
    :return:
    """
    component = np.zeros_like(image)
    mask = np.zeros_like(image)
    if len(approx) == 2:
        mask, component = draw_the_sq(approx, square_contour,mask, component, sq_log)
    else:
        mask, component = draw_the_stuff(approx, square_contour,mask, component, sq_log)

    return mask, component


def geometry_fun(contour, corners):
    topleft, botleft, botright, topright = corners
    moments = cv2.moments(contour)
    centre = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))

    diag = math.hypot(float(topleft[0]) - float(botright[0]), float(topleft[1]) - float(botright[1]))
    wid = math.hypot(float(topleft[0]) - float(topright[0]), float(topleft[1]) - float(topright[1]))
    hei = math.hypot(float(topleft[0]) - float(botleft[0]), float(topleft[1]) - float(botleft[1]))

    if diag ** 2 == wid ** 2 + hei ** 2:
        print('Everything is fine.')

    print('The diagonal of the rectangle is %d.' % diag)
    print('The width of the rectangle is %d.' % wid)
    print('The height of the rectangle is %d.' % hei)
    return(centre, wid, hei)


def get_square_coords(i, width, height, constants):
    x_coef = width / side
    y_coef = height / side
    wi1 = constants[0]
    wi2 = constants[1]
    he1 = constants[2]
    he2 = constants[3]
    coords = []

    if wi1 == wi2:
        if i[0] < centre[0]:
            x = int(i[0] + wi1 * x_coef)
            p = int(i[0] + he1 * x_coef)
            if i[1] < centre[1]:
                y = int(i[1] + wi1 * y_coef)
                q = int(i[1] + he1 * y_coef)
            else:
                y = int(i[1] - wi1 * y_coef)
                q = int(i[1] - he1 * y_coef)
        else:
            x = int(i[0] - wi1 * x_coef)
            p = int(i[0] - he1 * x_coef)
            if i[1] < centre[1]:
                y = int(i[1] + wi1 * y_coef)
                q = int(i[1] + he1 * y_coef)
            else:
                y = int(i[1] - wi1 * y_coef)
                q = int(i[1] - he1 * y_coef)
        res = ((x, y), (p, q))
    else:
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
        res = ((x, y), (p, q))
    return res


def geometry_of_white(image, list_of_corners, width, height, constants):
    # this finds white areas
    # constants are known from the palette sketch found in sample folder
    white = np.zeros_like(image)
    square_coords = []
    for i in list_of_corners:
        square_coords.append(get_square_coords(i, width, height, constants))
    # white can be seen if "panic regime" is on
    for sc in square_coords:
        cv2.rectangle(white, sc[0], sc[1], (255, 255, 255), -1)

    x = np.where(white == [255, 255, 255])[0]
    y = np.where(white == [255, 255, 255])[1]
    wh = []
    for i in range(len(x)):
        wh.append((x[i], y[i]))

    intensities = []
    for i in range(len(wh)):
        x, y = wh[i]
        intensities.append(image[x, y])
        white[x, y] = intensities[i]
    whites = np.unique(white)[1:]

    return whites, intensities, white


def geometry_of_color(image, list_of_corners, width, height, constants):
    # this finds coloured areas
    # constants are known from the palette sketch found in sample folder
    color = np.zeros_like(image)
    color_coords = []
    for i in list_of_corners:
        color_coords.append(get_square_coords(i, width, height, constants))

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


def colorwork(regime, img, corners, width, height, w_const, c_const, m_const, y_const):
    whites, intensities, white = geometry_of_white(img, corners, width, height, w_const)
    show_pic(whites, num)
    white_av, color_dev = whitecheck(whites)
    cy_int, cyan = geometry_of_color(img, corners, width, height, c_const)
    show_pic(cyan, num)
    ma_int, magenta = geometry_of_color(img, corners, width, height, m_const)
    show_pic(magenta, num)
    ye_int, yellow = geometry_of_color(img, corners, width, height, y_const)
    show_pic(yellow, num)
    # Comparing the retreived values
    cy = color_average(cy_int)
    ma = color_average(ma_int)
    ye = color_average(ye_int)

    return white_av, cy, ma, ye

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
    color = [(r / count), (g / count), (b / count)]
    return color


def info(array):
    a = type(array)
    b = array[0]
    c = array.shape

    return a, b, c


# Construct the argument parse and parse the arguments
if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='let the process begin')
    ap.add_argument('-i', '--image', required=True, help='Full path to the image')
    ap.add_argument('-p', '--panic', help='Show every image on each step and save it to the directory mentioned',
                    default=None)
    ap.add_argument('-j', '--json',
                    help='Path to the json parameters file with the constants required for the analysis',
                    default='const.json')
    args = vars(ap.parse_args())

    num = 0
    w_const, c_const, m_const, y_const, tolerance, side = pattern_pars(args['json'])
    img = cv2.imread(args['image'])
    contours, th2 = contours_selection_threshold(img)
    show_pic(th2, num)

    square = square_selection(contours, img, tolerance)

    # Checkpoint of contour sides
    approx, square_log = square_or_not(square)
    topleft, botleft, botright, topright = coords_check(approx, square_log)
    mask, component = shrink_the_mask(approx, square, img, square_log, tolerance)
    checkpoint_log = chpoint_check(img, mask, component, square_log, topleft, tolerance)
    corners = [topleft, botleft, botright, topright]
    centre, width, height = geometry_fun(square, corners)

    # Working with the color
    white_av, cy, ma, ye = colorwork(args['panic'], img, corners, width, height, w_const, c_const, m_const, y_const)
    print(cy, white_av)
    print(ma, white_av)
    print(ye, white_av)

    if cy[0] < ma[0]:
        if cy[0] < ye[0]:
            cyanred = True
        else:
            cyanred = False
    else:
        cyanred = False

    if ma[1] < cy[1]:
        if ma[1] < ye[1]:
            magentagreen = True
        else:
            magentagreen = False
    else:
        magentagreen = False

    if ye[1] < cy[1]:
        if ye[1] < ma[1]:
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
    # finding contour areas

    print("the end")
