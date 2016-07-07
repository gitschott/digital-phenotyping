#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

def dict_compare(d1, d2):
    d1_keys = set(d1.keys())
    d2_keys = set(d2.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
    same = set(o for o in intersect_keys if d1[o] == d2[o])
    return modified, same


# Read all the parameters


current = os.path.dirname(os.path.realpath(__file__))

snp_val = {}
exp_data = {}
with open(os.path.join(current, 'parameters_iris_rs.csv')) as csvfile:
    rs_param = csv.reader(csvfile, delimiter=';')
    headers = next(rs_param)
    for row in rs_param:
        snp_val[row[1]] = row[2],row[2]
        exp_data[row[1]] = row[2],'C'

modified, same = dict_compare(snp_val, exp_data)

print('modified :', modified)
print('same :', same)


# Detect minor alleles values

# Put values into model

# Estimate

# Predict

# Check prediction
