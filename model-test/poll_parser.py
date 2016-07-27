#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv
import os
import numpy as np

def impo(args=None):
    parser = argparse.ArgumentParser(description='Select poll input data')
    parser.add_argument('-p', '--poll',
                        help="the file that contains information on volunteers' phenotypes",
                        required='True')
    try:
        results = parser.parse_args()
        return (results.poll)
    except SystemExit:
        print("do something else")

def parse(file):
    strings = []
    path = os.getcwd()
    answers = open(file, 'r', encoding='utf-8')
    for q, line in enumerate(answers):
        if q == 0:
            header = str.split(line, sep='"')
        else:
            vals = str.split(line, sep=',')
            vals = vals [3:]
            strings.append(vals)
    os.chdir(path)
    tab = np.array(strings)

    return header, tab

if __name__ == '__main__':
    file = impo()
    head, pli = parse(file)
    print(pli)