#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import csv

def import(args=None):
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
    answers = open(file, 'r', encoding='cp1252')
    for q, line in enumerate(answers):
        # exclude comment lines
        print(q)
        print(line)
        strings.append(line)
    os.chdir(path)

    return strings
