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





# Detect minor alleles values

# Put values into model

# Estimate

# Predict

# Check prediction
