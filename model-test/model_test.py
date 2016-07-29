#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import csv
import numpy as np
import pandas as pd
import math
import ast


# Print all the arguments given to the program
def check_arg(args=None):
    #
    parser = argparse.ArgumentParser(description='Choose analysis mode and input data')
    parser.add_argument('-m', '--mode',
                        help='mode of analysis: eye, hair, skin',
                        required='True',
                        default='total')
    parser.add_argument('-v', '--vcf',
                        help='genotyping data path',
                        required='True')
    parser.add_argument('-p', '--param',
                        help='parameters data path, (default: self-report/ directory in repo)',
                        default='self-report/')
    parser.add_argument('-s', '--silent',
                        help='on / off -- print the output or not',
                        default='on')
    results = parser.parse_args()
    if results is None:
        print("You need to specify mode of analysis and a path"
              "to the vcf file. For detailed information please refer to README")
    return (results.mode,
            results.vcf,
            results.param,
            results.silent)


# Get the list rs relevant for particular mode of the analysis
def get_rs(mode, path_to_param):
    if path_to_param != 'self-report/':
        usepath = path_to_param
    else:
        usepath = os.path.abspath('self-report/')
    for file in os.listdir(usepath):
        # select eye / hair / skin -marks.txt
        if file.startswith(mode):
            path = os.getcwd()
            os.chdir('self-report/')
            f = open(file, 'r', encoding='cp1252')
            rs = [line.split('\n') for line in f.readlines()]
            # remove the comment
            del rs[len(rs) - 1]
            rsnp = []
            # make rs list
            for i in rs:
                rsnp.append(i[0])
            # remove the blank
            del rsnp[len(rsnp) - 1]
            os.chdir(path)

            return rsnp


def labelling(str_filename):
    # makes an adequate label out of filename
    file = str_filename[::-1]
    new = file[:10]
    file = new[::-1]
    file = file[:6]
    return file


def _parse_vcf(file):
    strings = []
    fl = []
    path = os.getcwd()
    vicief = open(file, 'r', encoding='cp1252')
    for q, line in enumerate(vicief):
        # exclude comment lines
        if line.startswith('#'):
            pass
        else:
            # analyse only actual informative lines
            if line.startswith('chr'):
                file = labelling(file)
                string = str.split(line, sep='\t')
                filt = string[6]
                rs = string[2]
                ref = string[3]
                alt = string[4]
                gt = str.split(string[9], sep=':')
                gt = gt[0]
                lst = [file, filt, rs, ref, alt, gt]
                strings.append(lst)
    os.chdir(path)
    return strings


def _value_setter(string):
    ref = string[3]
    gent = str.split(string[5], sep='/')
    alt = str.split(string[4], sep=',')
    nucl = {'A': 's1', 'T': 's1', 'G': 's2', 'C': 's2'}
    if gent[0] == gent[1]:
        index = int(gent[0]) - 1
        letter = alt[index]
        if nucl[ref] == nucl[letter]:
            val = float(0)
        else:
            val = float(2)
    else:
        index = int(gent != 0) - 1
        letter = alt[index]
        if nucl[ref] == nucl[letter]:
            val = float(0)
        else:
            val = float(1)

    return val


# Grep the particular snps relevant for the analysis (from vcf-containing folder)
def get_snp(vcf, snp):
    bs = {}
    data = _parse_vcf(vcf)
    for c, string in enumerate(data):
        for i in snp:
            s = string[2]
            result = re.match(i, s)
            if result is not None:
            # quality filter
                if string[1] == 'PASS':
                    lab = (string[0], s)
                    val = _value_setter(string)
                    bs[lab] = val
                else:
                    pass
            else:
                pass

    return bs


# Grep the parameters for a model, parameters is a csv file
def param(path_to_param, mode):
    if path_to_param != 'self-report/':
        usepath = path_to_param
    else:
        usepath = os.path.abspath('self-report/')
    snp_val = {}
    path = os.getcwd()
    os.chdir(usepath)
    if mode == 'eye':
        with open('parameters_iris_rs.csv') as csvfile:
            rs_param = csv.reader(csvfile, delimiter=';')
            headers = next(rs_param)
            for row in rs_param:
                snp_val[row[1]] = row[2:5]
    elif mode == 'hair':
        with open('parameters_hair4_rs.csv') as csvfile:
            rs_param = csv.reader(csvfile, delimiter=';')
            headers = next(rs_param)
            for row in rs_param:
                snp_val[row[1]] = row[2:6]
    else:
        print('Nothing to analyze')
    alpha = []
    if mode == 'eye':
        with open('parameters_iris_alpha.csv') as csvfile:
            rs_param = csv.reader(csvfile, delimiter=';')
            headers = next(rs_param)
            headers = next(rs_param)
            for row in rs_param:
                alpha.append(row)
        os.chdir(path)
    elif mode == 'hair':
        with open('parameters_hair4_alpha.csv') as csvfile:
            rs_param = csv.reader(csvfile, delimiter=';')
            headers = next(rs_param)
            headers = next(rs_param)
            for row in rs_param:
                alpha.append(row)
        os.chdir(path)
    else:
        print('Nothing to analyze')
    return snp_val, alpha


def _sumgetter(lst_beone, lst_betwo):
    tot1 = round(sum(lst_beone))
    tot2 = round(sum(lst_betwo))
    sums_lst = [tot1, tot2]
    return sums_lst


def eye_estim(dict_of_analyzed, parameters_for_snp):
    beone = []
    betwo = []
    for a in dict_of_analyzed:
        rs = str.split(a[1], sep=";")
        for v in parameters_for_snp:
            # match proper parameters
            result = re.match(rs[0], v)
            if result is not None:
                # implement the model
                mf = dict_of_analyzed[a]
                beta1 = (parameters_for_snp[v])[1]
                beta2 = (parameters_for_snp[v])[2]
                b1 = float(beta1)
                b2 = float(beta2)
                beone.append(mf * b1)
                betwo.append(mf * b2)
    coefs = _sumgetter(beone, betwo)

    return coefs


def hair_estim(dict_of_analyzed, parameters_for_snp):
    beone = []
    betwo = []
    betre = []
    for a in dict_of_analyzed:
        rs = str.split(a[1], sep=";")
        for v in parameters_for_snp:
            # match proper parameters
            result = re.match(rs[0], v)
            if result is not None:
                # implement the model
                mf = dict_of_analyzed[a]
                beta1 = float((parameters_for_snp[v])[1])
                beta2 = float((parameters_for_snp[v])[2])
                beta3 = float((parameters_for_snp[v])[3])
                beone.append(mf * b1)
                betwo.append(mf * b2)
                betre.append(mf * b3)
    coefs = [round(sum(beone), 4), round(sum(betwo), 4), round(sum(betre), 4)]
    return coefs

def snp_estim(dict_of_analyzed, parameters_for_snp, mode):
    if mode == 'eye':
        coefs = eye_estim(dict_of_analyzed, parameters_for_snp)
    elif mode == 'hair':
        coefs = hair_estim(dict_of_analyzed, parameters_for_snp)

    return coefs


def get_prob(list_w_sums, alpha_val_model):
    alp = alpha_val_model[0]
    beta1 = math.exp(float(list_w_sums[0]) + float(alp[0]))
    beta2 = math.exp(float(list_w_sums[1]) + float(alp[1]))
    beta1 = round(beta1, 4)
    beta2 = round(beta2, 4)
    prob = [beta1, beta2]
    print(prob)

    return prob


def eyecolor_probs(prob_list):
    col = ['blue', 'intermed', 'brown']
    pblue = prob_list[0] / (1 + prob_list[0] + prob_list[1])
    pint = prob_list[1] / (1 + prob_list[0] + prob_list[1])
    pbrown = 1 - pblue - pint
    colors = {col[0]: pblue, col[1]: pint, col[2]: pbrown}
    probability = [pblue, pint, pbrown]

    return colors


def verbose_pred_eyes(probability):
    print('Eyes are: ', 'blue', probability['blue'],
          'intermediate', probability['intermed'], 'brown', probability['brown'])


def executable(m, v, p, s):
    snip = get_rs(m, p)

    if s == 'off':
        if snip is None:
            print('Something whent wrong when we tried to get to rs.')
        else:
            print('You are predicting pigmentation of', m)
            print('Your rs list includes %d elements' % len(snip))

    # selection of snps in a way required for a model
    bs_snp = get_snp(v, snip)
    if s == 'off':
        print('You are now analysing %d SNPs.' % len(bs_snp))

    # Read all the parameters
    coefficients = param(p, m)
    beta, alpha = coefficients
    sums = snp_estim(bs_snp, beta, m)

    prob = get_prob(sums, alpha)

    # # # Counting three probs
    probs = eyecolor_probs(prob)

    return probs


if __name__ == '__main__':
    mode, vcf, par, silent = check_arg()
    if silent == 'off':
        print('mode =', mode)
        print('vcf =', vcf)
        print('param =', par)
        print('silent mode =', silent)
    probabilities = executable(mode, vcf, par, silent)

    if silent == 'off':
        verbose_pred_eyes(probabilities)