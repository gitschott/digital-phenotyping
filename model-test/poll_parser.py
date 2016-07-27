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
                        required='True')
    try:
        results = parser.parse_args()
        return (results.poll, results.sample)
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
            if vals[0] == '':
                pass
            else:
                vals = vals [3:]
                name = vals[0]
                sex = vals[1]
                age = vals[2]
                nat = vals[3]

                # Select the label
                name = name.upper()
                if len(name) == 4:
                    name = "-00".join(name.rsplit("-", 1))
                elif len(name) == 5:
                    name = "-0".join(name.rsplit("-", 1))
                else:
                    pass

                # Select the sex
                if sex.startswith('М'):
                    sex = 'male'
                else:
                    sex = 'female'

                # Select the nationality
                nat = str.split(nat, sep='/')
                if len(nat) == 2:
                    natio = nat[1]
                else:
                    natio = 'not defined nation.'

                vals = [name, sex, age, natio]
                strings.append(vals)
        os.chdir(path)
        tab = np.array(strings)

    return header, tab, name

def story(array, name):
    for i in array:
        result = re.match(i[0], name)
        if result is not None:
            print('The data provided on:', name, 'is the following.', name, 'is a', i[1], i[2], 'years old that belongs to', i[3])


if __name__ == '__main__':
    file, s = impo()
    head, pli, name = parse(file)
    story(pli, s)