#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import numpy as np
import re

def impo(args=None):
    parser = argparse.ArgumentParser(description='Select poll input data')
    parser.add_argument('-p', '--poll',
                        help="the file that contains information on volunteers' phenotypes",
                        required='True')
    parser.add_argument('-s', '--sample',
                        help="sample of interest",
                        default='all')
    results = parser.parse_args()
    return (results.poll, results.sample)

def _label(name):
    # Select the label
    name = name.upper()
    if len(name) == 4:
        name = "-00".join(name.rsplit("-", 1))
    elif len(name) == 5:
        name = "-0".join(name.rsplit("-", 1))
    else:
        pass

    return name


def _malefe(value):
    # Select the sex
    if value.startswith('М'):
        sex = 'male'
    else:
        sex = 'female'
    return sex


def _nation(value):
    # Select the nationality
    nat = str.split(value, sep='/')
    if len(nat) == 2:
        natio = nat[1]
    else:
        natio = 'not defined nation.'

    return natio


def _eyecolor(list):
    eyesat = list[1].split("'")[0].split("/")[1]
    colors = str.split(list[0], sep=',')
    if len(colors) == 1:
        colors = colors[0]
        eyehue = str.split(colors, sep='/')[1]
        if eyehue == ' I have mixed eye color':
            eyehue = 'mixed'
    else:
        iris = []
        eyehue = 'mixed'
        for c in colors:
            hue = (str.split(c, sep='/')[1])
            iris.append(hue)

        eye = [iris, eyesat]
        return eye, eyehue


def parse(file):
    strings = []
    oc = []
    with open(file, 'r', encoding='utf-8') as answers:
        for line in answers:
            if line == 0:
                header = str.split(line, sep='"')
            else:
                vals = str.split(line, sep='\t')
                if vals[0]:
                    vals = vals[2:]
                    # _label is only required if the file has BS format
                    name = _label(vals[0])
                    sex = _malefe(vals[1])
                    age = vals[2]
                    nat = _nation(vals[3])
                    eyes = vals[4:7]
                    print(eyes)
                    color, hues = _eyecolor(eyes)
                    eycol, eysat = color
                    vals = [name, sex, age, nat, eycol, eysat]
                    original_colors = [name, hues, eysat]
                    strings.append(vals)
                    oc.append(original_colors)
    # TODO: EDIT THIS to a normal output
    tab = np.array(strings)

    return tab, name, oc


def verbose_res(line):
    # line is a list of results of interpretation
    # of a poll and a model
    # the function compares and verbalises them both
    print('The data provided on:', line[0], 'is the following.', line[0], 'is a', line[1], line[2],
          'years old that belongs to', line[3])
    if line[4] == 'mixed':
        print(line[0], 'eye color is', line[4])
    else:
        print(line[0], 'eye color is', line[5], line[4])


def story(array, name):
    result = []
    if name != 'all':
        for lifestory_string in array:
            if lifestory_string[0] == name:
                result.append(lifestory_string)
    else:
        for lifestory_string in array:
            result.append(lifestory_string)
    return result


def whole_poll(file, s):
    total, sample_lab, iris_color = parse(file)
    _ = story(total, s)

    return total, iris_color


if __name__ == '__main__':
    file, sample = impo()
    table, iris = whole_poll(file, sample)
    for i in table:
        verbose_res(i)
