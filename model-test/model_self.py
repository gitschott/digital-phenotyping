#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv

def dict_simplify(dict):
    d2_keys = set()
    deetoo = dict.keys()
    for d in deetoo:
        val = (d[1])
        d2_keys.add(val)
    return d2_keys


def dict_compare(d1, d2, d2_keys):
    d1_keys = set(d1.keys())
    intersect_keys = d1_keys.intersection(d2_keys)
    modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
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
        print(headers)
        print(row)
        snp_val[row[1]] = row[2],row[2]
        exp_data['BS-004',row[1]] = row[2],'C'

exp_keys = dict_simplify(exp_data)

modified, same = dict_compare(snp_val, exp_data, exp_keys)

print('modified :', modified)
print('same :', same)


# Detect minor alleles values

# Put values into model

# Estimate

# Predict

# Check prediction
