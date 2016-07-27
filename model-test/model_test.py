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
    results = parser.parse_args()
    if results is None:
        print("You need to specify mode of analysis and a path\
         to the vcf file. For detailed information please refer to README")
    return (results.mode,
            results.vcf,
            results.param)


# Get the list rs relevant for particular mode of the analysis
def get_rs(mode, path_to_param):
    for file in os.listdir(os.path.abspath('self-report/')):
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
                    gt1, gt2 = str.split(string[5], sep='/')
                    if gt1 == gt2:
                        gt = gt1,
                        if gt == 0:
                            val = float(0)
                        else:
                            val = float(2)
                    else:
                        val = float(1)
                    bs[lab] = val
                else:
                    pass
            else:
                pass

    return bs


# Grep the parameters for a model, parameters is a csv file
def param(path_to_param, mode):
    snp_val = {}
    path = os.getcwd()
    os.chdir(path_to_param)
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


def snp_estim_eye(dict_of_analyzed, parameters_for_snp):
    coefs = {}
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
                coefs[a[0], v] = [mf * b1, mf * b2]
    bi1 = 0
    bi2 = 0
    for key, value in iter(coefs):
        b1 = coefs[key, value]
        bi1 += b1[0]
        bi2 += b1[1]

    coef_list = [beta1, beta2]

    return coef_list


def snp_estim_h4(samples, dict_of_analyzed, parameters_for_snp):
    coefs = {}
    for a in dict_of_analyzed:
        for s in samples:
            result = re.match(a[0], s)
            if result is not None:
                for v in parameters_for_snp:
                    result = re.match(a[1], v)
                    if result is not None:
                        minor, m_freq = dict_of_analyzed[a]
                        minor_mod, beta1, beta2, beta3 = parameters_for_snp[v]
                        mf = float(m_freq)
                        b1 = float(beta1)
                        b2 = float(beta2)
                        b3 = float(beta3)
                        # coefs[s, v] = [float(m_freq) * float(beta1), float(m_freq) * float(beta2)]
                        if minor == minor_mod:
                            coefs[s, v] = [mf * b1, mf * b2, mf * b3]
                        else:
                            nbases = {'A': 'C1', 'T': 'C1', 'G': 'C2', 'C': 'C2'}
                            if nbases[minor] == nbases[minor_mod]:
                                coefs[s, v] = [mf * b1, mf * b2, mf * b3]
                            else:
                                mf = 0
                                coefs[s, v] = [mf * b1, mf * b2]

    coef_list = []
    for key, value in iter(coefs):
        beta = coefs[key, value]
        temp = [key, value, beta[0], beta[1], beta[2]]
        coef_list.append(temp)
    df = pd.DataFrame(coef_list)
    df = df.groupby(0)[[2, 3]].sum()

    return df


def get_prob(list_w_sums, alpha_val_model):
    alp = alpha_val_model[0]
    beta1 = math.exp(float(list_w_sums[0]) + float(alp[0]))
    beta2 = math.exp(float(list_w_sums[1]) + float(alp[1]))
    prob = [beta1, beta2]

    return prob


def eyecolor_probs(prob_list):
    col = ['blue', 'intermed', 'brown']
    pblue = prob_list[0] / (1 + prob_list[0] + prob_list[1])
    pint = prob_list[1] / (1 + prob_list[0] + prob_list[1])
    pbrown = 1 - pblue - pint
    colors = {col[0]: pblue, col[1]: pint, col[2]: pbrown}
    probability = [pblue, pint, pbrown]
    print('Eyes are: ', 'blue', probability[0], 'intermediate', probability[1], 'brown', probability[2])

    return colors


def executable(m, v, p):
    print('mode =', m)
    print('vcf =', v)
    print('param =', p)
    snip = get_rs(m, p)

    if snip is None:
        print('Something whent wrong when we tried to get to rs.')
    else:
        print('You are predicting pigmentation of', m)
        print('Your rs list includes %d elements' % len(snip))

    # selection of snps in a way required for a model
    bs_snp = get_snp(v, snip)
    print('You are now analysing %d SNPs.' % len(bs_snp))

    # Read all the parameters
    if m == 'eye':
        beta, alpha = param(p, m)
    elif m == 'hair':
        beta_eye, alpha_eye = param(p, m)
        beta_hair, alpha_hair = param(p, m)
    else:
        print("It is not possible yet")

    if m == 'eye':
        sums = snp_estim_eye(bs_snp, beta)
    elif m == 'hair':
        sums_eye = snp_estim_eye(samples_eye, analysis, beta)
        sums_hair = snp_estim_h4(samples_hair, analysis, beta)
    else:
        print("It is not possible yet")

    prob = get_prob(sums, alpha)

    # # # Counting three probs
    probs = eyecolor_probs(prob)

    return probs


if __name__ == '__main__':
    m, v, p = check_arg()
    probabilities = executable(m, v, p)