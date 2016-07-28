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
    try:
        results = parser.parse_args()
        return (results.poll, results.sample)
    except SystemExit:
        print("do something else")

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


def most_common(lst):
    return max(set(lst), key=lst.count)


def _eyecolor(list):
    saturation = str.split(list[1], sep="'")
    saturation = saturation[0]
    saturation = str.split(saturation, sep="/")
    eyesat = saturation[1]
    colors = str.split(list[0], sep=',')
    if len(colors) == 1:
        colors = colors[0]
        eyehue = str.split(colors, sep='/')
        eyehue = eyehue[1]
        eyehues = eyehue
        if eyehue == ' I have mixed eye color':
            eyehue = 'mixed'
    else:
        eyehues = []
        eyehue = 'mixed'
        for c in colors:
            hue = (str.split(c, sep='/')[1])
            eyehues.append(hue)

    eye = [eyehue, eyesat]
    return eye, eyehues


def parse(file):
    strings = []
    oc = []
    path = os.getcwd()
    answers = open(file, 'r', encoding='utf-8')
    for q, line in enumerate(answers):
        if q == 0:
            header = str.split(line, sep='"')
        else:
            vals = str.split(line, sep='\t')
            if vals[0] == '':
                pass
            else:
                vals = vals [2:]
                name = _label(vals[0])
                sex = _malefe(vals[1])
                age = vals[2]
                nat = _nation(vals[3])
                eyes = vals[4:7]
                eye, hues = _eyecolor(eyes)
                eycol, eysat = eye
                vals = [name, sex, age, nat, eycol, eysat]
                original_colors = [name, hues, eysat]
                strings.append(vals)
                oc.append(original_colors)
        os.chdir(path)
        tab = np.array(strings)

    return tab, name, oc


def verbose_res(line):
    print('The data provided on:', line[0], 'is the following.', line[0], 'is a', line[1], line[2],
          'years old that belongs to', line[3])
    if line[4] == 'mixed':
        print(line[0], 'eye color is', line[4])
    else:
        print(line[0], 'eye color is', line[5], line[4])


def story(array, name):
    result = []
    if name != 'all':
        for i in array:
            result = re.match(i[0], name)
            if result is not None:
                result.append(i)
    else:
        for i in array:
            result.append(i)
    return result


def whole_poll(file, s):
    total, sample_lab, iris_color = parse(file)
    stop = story(total, s)

    return total, iris_color


if __name__ == '__main__':
    file, s = impo()
    table, iris = whole_poll(file, s)
    for i in table:
        verbose_res(i)
