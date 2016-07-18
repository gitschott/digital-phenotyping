#!/usr/bin/env python
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
    parser.add_argument('-p', '--phen',
                        help='phenotyping and mode parameters data path',
                        required='True')

    results = parser.parse_args(args)
    return (results.mode,
            results.vcf,
            results.phen)


# Get the list rs relevant for particular mode of the analysis
def get_rs(mode, path_to_rs_list):
    for file in os.listdir(os.path.abspath(path_to_rs_list)):
        # select eye / hair / skin -marks.txt
        if file.startswith(mode):
            path = os.getcwd()
            os.chdir(path_to_rs_list)
            f = open(file, 'r')
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


# Grep the particular snps relevant for the analysis (from vcf-containing folder)
def get_snp(vcf, snp):
    bs = {}
    for file in os.listdir(os.path.abspath(vcf)):
        path = os.getcwd()
        os.chdir(vcf)
        vicief = open(file, 'r', encoding='cp1252')
        for q, line in enumerate(vicief):
            # exclude comment lines
            if line.startswith('#'):
                pass
            else:
                # analyse only actual informative lines
                if line.startswith('chr'):
                    string = str.split(line, sep='\t')
                    for s in string:
                        # select rs of interest
                        if s.startswith('rs'):
                            for i in snp:
                                result = re.match(i, s)
                                if result is not None:
                                    # quality filter
                                    if string[6] == 'PASS':
                                        ref = string[3]
                                        if len(string[4]) > 1:
                                            alt = str.split(string[4], sep=',')
                                            af = str.split(string[9], sep=':')
                                            names = str.split(string[8], sep=':')
                                            ind = names.index("AF")
                                            freq = str.split(af[ind], sep=',')
                                            if freq[1:] == freq[:-1]:
                                                # key in the dict takes first 6 symbols of a file that is id
                                                bs[file[:6], i] = ref, float(0)
                                            else:
                                                for f in freq:
                                                    num = float(f)
                                                    if num == 0:
                                                        pass
                                                    else:
                                                        if num == 1:
                                                            num = str(int(num))
                                                            ind_f = freq.index(num)
                                                            bs[file[:6], i] = alt[ind_f], float(2)
                                                        elif num > 0:
                                                             f = max(freq)
                                                             ind_f = freq.index(f)
                                                             bs[file[:6], i] = alt[ind_f], float(1)
                                                        else:
                                                            print("WRONG", num)
                                        else:
                                            alt = string[4]
                                            af = str.split(string[9], sep=':')
                                            names = str.split(string[8], sep=':')
                                            ind = names.index("AF")
                                            freq = af[ind]
                                            if freq == 0:
                                                bs[file[:6], i] = ref, float(0)
                                            elif freq == 1:
                                                bs[file[:6], i] = alt, float(2)
                                            else:
                                                bs[file[:6], i] = alt, float(1)
                                    else:
                                        pass
                                else:
                                    pass
        os.chdir(path)

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


def grep_snip(parameters_for_snp, sample_dictionary):
    analyze = {}
    for v in parameters_for_snp:
        for k in sample_dictionary.keys():
            result = re.match(v, k[1])
            if result is not None:
                analyze[k] = sample_dictionary[k]

    samples = []
    for a in analyze:
        sample = a[0]
        samples.append(sample)
    samples = list(set(samples))

    return samples, analyze


def snp_estim_eye(samples, dict_of_analyzed, parameters_for_snp):
    coefs = {}
    for a in dict_of_analyzed:
        for s in samples:
            result = re.match(a[0], s)
            if result is not None:
                for v in parameters_for_snp:
                    result = re.match(a[1], v)
                    if result is not None:
                        minor = (dict_of_analyzed[a])[0]
                        m_freq = (dict_of_analyzed[a])[1]
                        mf = float(m_freq)
                        minor_mod = (parameters_for_snp[v])[0]
                        beta1 = (parameters_for_snp[v])[1]
                        beta2 = (parameters_for_snp[v])[2]
                        b1 = float(beta1)
                        b2 = float(beta2)
                        # coefs[s, v] = [float(m_freq) * float(beta1), float(m_freq) * float(beta2)]
                        if minor == minor_mod:
                            print('Expected value for ', v, minor)
                            coefs[s, v] = [mf * b1, mf * b2]
                        else:
                            nbases = {'A':'R', 'G':'R', 'T':'Y', 'C':'Y'}
                            if nbases[minor] == nbases[minor_mod]:
                                print('Unexpected yet analyzed value for ', v, minor, minor_mod)
                                coefs[s, v] = [mf * b1, mf * b2]
                            else:
                                print('Unexpected value for ', v, minor, minor_mod)


    coef_list = []
    for key, value in iter(coefs):
        beta = coefs[key, value]
        temp = [key, value, beta[0], beta[1]]
        coef_list.append(temp)
    df = pd.DataFrame(coef_list)
    df = df.groupby(0)[[2, 3]].sum()

    return df

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
                        print(beta1, beta1[0])
                        b1 = float(beta1)
                        b2 = float(beta2)
                        b3 = float(beta3)
                        # coefs[s, v] = [float(m_freq) * float(beta1), float(m_freq) * float(beta2)]
                        if minor == minor_mod:
                            print('Expected value for ', v, minor)

                            coefs[s, v] = [mf * b1, mf * b2, mf * b3]
                        else:
                            nbases = {'A':'R', 'G':'R', 'T':'Y', 'C':'Y'}
                            if nbases[minor] == nbases[minor_mod]:
                                print('Unexpected yet analyzed value for ', v, minor, minor_mod)
                                coefs[s, v] = [mf * b1, mf * b2, mf * b3]
                            else:
                                print('Unexpected value for ', v, minor, minor_mod)


    coef_list = []
    for key, value in iter(coefs):
        beta = coefs[key, value]
        temp = [key, value, beta[0], beta[1], beta[2]]
        coef_list.append(temp)
    df = pd.DataFrame(coef_list)
    df = df.groupby(0)[[2, 3]].sum()

    return df


def get_prob(df_sums, alpha_val_model):
    prob = pd.DataFrame()
    for index, row in df_sums.iterrows():
        alp = alpha_val_model[0]
        beta1 = math.exp(float(row[2]) + float(alp[0]))
        beta2 = math.exp(float(row[3]) + float(alp[1]))
        prob = prob.append([[index, beta1, beta2]])

    return prob

def eyecolor_probs(prob_df):
    colors = pd.DataFrame()
    for index, row in prob_df.iterrows():
        pblue = row[1] / (1 + row[1] + row[2])
        pint = row[2] / (1 + row[1] + row[2])
        pbrown = 1 - pblue - pint
        colors.append([row[0], pblue, pint, pbrown])
        # print('Probabilities of getting blue / intermediate / brown eyecolor for sample', row[0])
        # print(pblue, pint, pbrown)
        probability = [pblue, pint, pbrown]
        col = ['blue', 'intermed', 'brown']
        ind = probability.index(max(probability))
        if col[ind] == 'blue':
            print('The prediction for eye color is :', row[0], 'eyes are', col[ind])

    return colors


if __name__ == '__main__':
    m, v, p = check_arg(sys.argv[1:])
    print('mode =', m)
    print('vcf =', v)
    print('phen =', p)

    snip = get_rs(m, p)

    if snip is None:
        print('Something whent wrong when we tried to get to rs.')
    else:
        print('You are predicting pigmentation of', m)
        print('Your rs list includes %d elements' % len(snip))

    # selection of snps in a way required for a model
    bs_snp = get_snp(v, snip)
    print('You are now analysing %d cases.' % len(bs_snp))

    # Read all the parameters
    if m == 'eye':
        beta, alpha = param(p, m)
    elif m == 'hair':
        beta_eye, alpha_eye = param(p, m)
        beta_hair, alpha_hair = param(p, m)
    else:
        print("It is not possible yet")

    if m == 'eye':
        samples, analysis = grep_snip(beta, bs_snp)
    elif m == 'hair':
        samples_eye, analysis = grep_snip(beta_eye, bs_snp)
        samples_hair, analysis = grep_snip(beta_hair, bs_snp)
    else:
        print("It is not possible yet")

    if m == 'eye':
        sums = snp_estim_eye(samples, analysis, beta)
    elif m == 'hair':
        sums_eye = snp_estim_eye(samples_eye, analysis, beta)
        sums_hair = snp_estim_h4(samples_hair, analysis, beta)
    else:
        print("It is not possible yet")

    prob = get_prob(sums, alpha)

# # # Counting three probs
    probs = eyecolor_probs(prob)
#
#     ## Compare the results


