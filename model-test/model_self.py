#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import csv


# Read all the parameters


current = os.path.dirname(os.path.realpath(__file__))

snp_val = {}
with open(os.path.join(current, 'parameters_iris_rs.csv')) as csvfile:
    rs_param = csv.reader(csvfile, delimiter=';')
    headers = next(rs_param)
    print(type(rs_param))
    for row in rs_param:
        snp_val[row[1]] = row[2],row[2]

print(snp_val)

# Detect minor alleles values

# Put values into model

# Estimate

# Predict

# Check prediction
