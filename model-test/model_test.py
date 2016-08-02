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
                    if len(line) > 1  and not line.startswith('#'):
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
                        lst = [lab, rs, ref, alt, gt]
                        strings.append(lst)
    return strings


def _value_setter(lst_from_vcf_string):
    # getting the value of genotype
    ref = lst_from_vcf_string[2]
    gent = str.split(lst_from_vcf_string[4], sep='/')
    alt = str.split(lst_from_vcf_string[3], sep=',')
    letters = [ref, alt[0], alt[1], alt[2]]
    nucl = {'A': 's1', 'T': 's1', 'G': 's2', 'C': 's2'}
    # in model complementary nucleotides have equal input
    if gent[0] == gent[1]:
        if int(gent[0]) == 0:
            val = float(0)
        else:
            val = float(2)
    else:
        alt1 = int(gent[0])
        alt2 = int(gent[1])
        if nucl[letters[alt1]] == nucl[letters[alt2]]:
            if nucl[ref] == nucl[letters[alt1]]:
                val = float(0)
            else:
                val = float(1)
        else:
            val = float(1)
            return val


# Grep the particular snps relevant for the analysis (from vcf-containing folder)
def get_snp(vcf_file, snp_list):
    # dictionary of values
    bs = {}
    data = _parse_vcf(vcf_file)
    for vcf_string in data:
        for snp in snp_list:
            s = vcf_string[1]
            s = str.split(s, sep=";")
            rs = s[0]
            # selection of mode-relevant rs
            if snp == rs:
                lab = (vcf_string[0], rs)
                val = _value_setter(vcf_string)
                bs[lab] = val
                # dictionary with genotype values
            else:
                pass
    return bs


# Grep the parameters for a model, parameters is a csv file
def param(path_to_param, mode):
    # path check
    newpath = os.path.abspath(path_to_param)
    # output dictionary of values
    beta_dict_snp_values = {}
    alpha_list = []
    # selectin beta parameters
    for file in os.listdir(newpath):
        file = os.path.join(newpath, file)
        with open(file) as csvfile:
            rs_param = csv.reader(csvfile, delimiter=';')
            headers = next(rs_param)
            name = os.path.splitext(file)[0]
            if name.startswith('par_beta_'):
                lab = re.sub('par_beta_', '', name)
                if mode == lab:
                    for row in rs_param:
                        beta_dict_snp_values[row[1]] = row[2:5]
            elif name.startswith('par_alpha_'):
                lab = re.sub('par_alpha_', '', name)
                if mode == lab:
                    for row in rs_param:
                        alpha_list.append(row)

    return beta_dict_snp_values, alpha_list


def _sumgetter(lst_beone, lst_betwo):
    tot1 = round(sum(lst_beone))
    tot2 = round(sum(lst_betwo))
    sums_lst = [tot1, tot2]
    return sums_lst


def eye_estim(dict_of_analyzed, dict_par_for_snp):
    # dict_of_analyzed contains genotypes as values and sample name and rs as labels
    # dict_par_for_snp contains beta parameters of IrisPlex model as values
    # and rs as labels
    beone = []
    betwo = []
    for a in dict_of_analyzed:
        rs = str.split(a[1], sep=";")
        for v in dict_par_for_snp:
            # match proper parameters
            if rs[0] == v:
                # implement the model
                mf = dict_of_analyzed[a]
                b1 = float((dict_par_for_snp[v])[1])
                b2 = float((dict_par_for_snp[v])[2])
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
            if rs[0] == v:
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


def executable(mode, vcf_file, path_to_param):
    snip = get_rs(mode, path_to_param)
    # selection of snps in a way required for a model
    bs_snp_dict = get_snp(vcf_file, snip)
    # Read all the parameters
    beta_dict, alpha_list = param(path_to_param, mode)
    probs = model_iris_plex(bs_snp_dict, beta_dict, mode, alpha_list)

    return probs


if __name__ == '__main__':
    mode, vcf, par, silent = check_arg()
    if silent == 'off':
        print('mode =', mode)
        print('vcf =', vcf)
        print('param =', par)
        print('silent mode =', silent)
    probabilities = executable(mode, vcf, par)
    if silent == 'off':
        print('You are predicting pigmentation of', mode)

    if silent == 'off':
        verbose_pred_eyes(probabilities)

