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

# List of constants for colors
tol = 0.97  # tolerance to contour area is 97 per cent
side = 480  # from five-sliced-shape script
w_const = [60, 60, 120, 120]
c_const = [170, 200, 90, 130]
m_const = [290, 320, 90, 130]
y_const = [230, 260, 90, 130]

# Contours selection facilitating function enhanced with the threshold


def contours_selection_threshold(image):
    # this is a primary step of image processing, its output is list of contours and a thresholded image array
    image = cv2.GaussianBlur(image, (5, 5), 0)  # blur is added to denoise the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # further operations are for binary pictures only
    ret2, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # thresholding step allows select the black frame
    tresh = np.copy(th2)  # when "panic regime" is on this picture is shown
    im, cnts, hier = cv2.findContours(th2, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    # getting the external contours

    return cnts, tresh


def square_selection(contours, image):
    # this selects contour of a black square
    areas = []
    # a and b are needed to calculate the square
    a = int(image.shape[0])
    b = int(image.shape[1])
    for c in contours:
        areas.append(cv2.contourArea(c))

    c_areas = np.asarray(areas)
    # biggest areas are the whole image and a square
    top = c_areas.argsort()[-2:][::-1]
    c = cv2.contourArea(contours[top[0]])

    if c >= tol*a*b:
        print('The biggest contour is the picture border, the second biggest contour was selected.')
        top_regime = True
    else:
        print('The biggest contour is not defined properly. The result might be unreliable.')
        top_regime = False

    # the choice of the contour depends on the square
    return top, top_regime


def shrink_the_mask(square_contour, image):
    # this gives the coordinates of a frame
    perimeter = cv2.arcLength(square_contour, True)  # finds closed contour
    if perimeter == 0:
        print('The square is not recognized.')
    epsilon = 0.1 * perimeter
    approx = cv2.approxPolyDP(square_contour, epsilon, True)

    if len(approx) > 4:
        print('The square is not recognized.')

    component = np.zeros_like(image)
    mask = np.zeros_like(image)

    if len(approx) == 2:
        print("It is a square!")
        # square marker is used further in analysis of white areas
        square = True
        x, z = approx
        x = x[0]
        y = (0, 0)
        z = z[0]
        h = (0, 0)
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

    else:
        square = False
        x, y, z, h = approx
        x = tuple(x[0])
        y = tuple(y[0])
        z = tuple(z[0])
        h = tuple(h[0])

        cv2.rectangle(component, (x[0], x[1]), (z[0], z[1]), (255, 255, 255), -1)
        cv2.drawContours(mask, square_contour, -1, (255, 255, 255), -1)
        component = cv2.cvtColor(component, cv2.COLOR_BGR2GRAY)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

        print('There are new coordinates of corners lying inside the contour of the square.')

        if mask[x[1], x[0]] == 255:
            print('Your square fits perfectly.')
            checkpoint = True
        else:
            print('The square is rotated or distorted.')
            checkpoint = False

    return x, y, z, h, mask, component, square, checkpoint


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
    ap = argparse.ArgumentParser(description="let the process begin")
    ap.add_argument("-i", "--image", required=True, help="Path to the image")
    ap.add_argument('-p', '--panic', action='store_true', help="Show every image on each step")
    args = vars(ap.parse_args())
    # ap = argparse.ArgumentParser(description ="Upload of the picture for the analysis, specify some details.")
    # ap.add_argument('-i','--image', required=True, help="Path to the image file")
    # # ap.add_argument('-c', '--contours', stored='store_true', help="Show image with contours")
    # # ap.add_argument('-i', '--save', stored='store_true', help="Save the result")
    # # args = vars(ap.parse_args(['-i','-c','-s']))
    # args = ap.parse_args()
    # print(args)
    # print(args[image])

    # Read the image and convert it to acceptable array for analysis
    img = cv2.imread(args['image'])  # image for analysis
    contours, th2 = contours_selection_threshold(img)
    top, top_regime = square_selection(contours, img)

    # Checkpoint of contour sides
    if top_regime:
        sq = int(top[1])
    else:
        sq = int(top[0])

    topleft, botleft, botright, topright, mask, component, square, checkpoint = shrink_the_mask(contours[sq], img)

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

    if args['panic']:
        cv2.imshow("img", cyan)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    ma_int, magenta = geometry_of_color(img, corners, wid, hei, m_const)

    if args['panic']:
        cv2.imshow("img", magenta)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    ye_int, yellow = geometry_of_color(img, corners, wid, hei, y_const)

    if args['panic']:
        cv2.imshow("img", yellow)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

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

    # cv2.drawContours(component, contours, sq, (255,255,255), -1)
    # cv2.imwrite("/test_images/badwhite3.jpg", white)
    # finding contour areas

print("the end")
