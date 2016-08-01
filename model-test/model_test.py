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
    parser.add_argument('-s', '--silent',
                        help='on / off -- print the output or not',
                        default='off')
    results = parser.parse_args()

    return (results.mode,
            results.vcf,
            results.param,
            results.silent)


# Get the list rs relevant for particular mode of the analysis
def get_rs(mode, path_to_param):
    usepath = os.path.abspath(path_to_param)
    rsnp = []
    for file in os.listdir(usepath):
        # select eye / hair / skin -marks.txt
        if file.startswith(mode):
            address = os.path.abspath(os.path.join(usepath, file))
            with open(address, 'r', encoding='cp1252') as f:
                for line in f:
                    # exclude comment lines
                    if line and not line.startswith('#'):
                        line = str.strip(line)
                        rsnp.append(line)

    return rsnp


def _parse_vcf(file):
    # reading the vcf sample
    strings = [] # list that is filled with output
    with open(file, 'r', encoding='cp1252') as vicief:
        lab = os.path.basename(file)
        for q, line in enumerate(vicief):
            # exclude comment lines
            if line.startswith('chr'):
                string = str.split(line, sep='\t')
                if string[6] == 'PASS':
                    rs = string[2]
                    if rs != '.':
                        ref = string[3]
                        alt = string[4]
                        gt = str.split(string[9], sep=':')
                        gt = gt[0]
                        # list containing name of sample, rs,
                        # reference and alternative nucleotides and genotype
                        lst = [file, rs, ref, alt, gt]
                        strings.append(lst)
    return strings


def _value_setter(lst_from_vcf_string):
    # getting the value of genotype
    ref = lst_from_vcf_string[2]
    gent = str.split(lst_from_vcf_string[4], sep='/')
    alt = str.split(lst_from_vcf_string[3], sep=',')
    # in model complementary nucleotides have equal input
    nucl = {'A': 's1', 'T': 's1', 'G': 's2', 'C': 's2'}
    if gent[0] == gent[1]:
        # homozygote
        index = int(gent[0]) - 1
        letter = alt[index]
        if gent[0] == 0:
            val = float(0)
        else:
            if nucl[ref] == nucl[letter]:
                # no significant substitutions
                val = float(0)
            else:
                # homozygote is completely different from the reference
                val = float(2)
    else:
        # heterozygote
        index = int(gent != 0) - 1
        letter = alt[index]
        if nucl[ref] == nucl[letter]:
            # filter for complementary nucleotides
            val = float(0)
        else:
            val = float(1)

    return val


# Grep the particular snps relevant for the analysis (from vcf-containing folder)
def get_snp(vcf, snp):
    # dictionary of values
    bs = {}
    data = _parse_vcf(vcf)
    for c, string in enumerate(data):
        for i in snp:
            s = string[1]
            # selection of mode-relevant rs
            result = re.match(i, s)
            if result is not None:
                lab = (string[0], s)
                val = _value_setter(string)
                # dictionary with genotype values
                bs[lab] = val
            else:
                pass

    return bs


# Grep the parameters for a model, parameters is a csv file
def param(path_to_param, mode):
    # path check
    newpath = os.path.abspath(path_to_param)
    # output dictionary of values
    snp_val = {}
    alpha = []
    # selectin beta parameters
    for file in os.listdir(newpath):
        name = os.path.splitext(file)
        name = name[0]
        if name.startswith('par_beta_'):
            lab = re.sub('par_beta_', '', name)
            if mode == lab:
                file = os.path.join(newpath, file)
                with open(file) as csvfile:
                    rs_param = csv.reader(csvfile, delimiter=';')
                    headers = next(rs_param)
                    for row in rs_param:
                        snp_val[row[1]] = row[2:5]
        elif name.startswith('par_alpha_'):
            lab = re.sub('par_alpha_', '', name)
            if mode == lab:
                file = os.path.join(newpath, file)
                with open(file) as csvfile:
                    rs_param = csv.reader(csvfile, delimiter=';')
                    headers = next(rs_param)
                    for row in rs_param:
                        alpha.append(row)
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

    return prob


def eyecolor_probs(prob_list):
    col = ['blue', 'intermed', 'brown']
    pblue = prob_list[0] / (1 + prob_list[0] + prob_list[1])
    pint = prob_list[1] / (1 + prob_list[0] + prob_list[1])
    pbrown = 1 - pblue - pint
    colors = {col[0]: pblue, col[1]: pint, col[2]: pbrown}
    probability = [pblue, pint, pbrown]

    return colors


def model_iris_plex(snp_sample_dict, beta_coefficients, mode_of_analysis,
                    alpha_parameters):
    sums = snp_estim(snp_sample_dict, beta_coefficients, mode_of_analysis)
    prob = get_prob(sums, alpha_parameters)
    # # # Counting three probs
    probs = eyecolor_probs(prob)
    return probs


def verbose_pred_eyes(probability):
    print('Eyes are: ', 'blue', probability['blue'],
          'intermediate', probability['intermed'], 'brown', probability['brown'])


def executable(m, v, p, s):
    snip = get_rs(m, p)
    # selection of snps in a way required for a model
    bs_snp = get_snp(v, snip)
    # Read all the parameters
    coefficients = param(p, m)
    beta, alpha = coefficients
    probs = model_iris_plex(bs_snp, beta, m, alpha)

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
        print('You are predicting pigmentation of', mode)

    if silent == 'off':
        verbose_pred_eyes(probabilities)

