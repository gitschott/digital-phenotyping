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
import json


class Parameters:
    def __init__(self, jsondata):
        self.alpha1 = jsondata['alpha1']
        self.alpha2 = jsondata['alpha2']

    def __repr__(self):
        return "params a1={0}, a2={1}".format(self.alpha1, self.alpha2)


class Loci(object):
    def __init__(self, name, minor_allele, beta1, beta2,
                 strand, rank):
        self.name = name
        self.minor_allele = minor_allele
        self.beta1 = beta1
        self.beta2 = beta2
        self.strand = strand
        self.rank = rank

    def __repr__(self):
        return ', '.join(['{0}:{1}'.format(x, y) for x, y in self.__dict__.items()])


def check_arg():
    parser = argparse.ArgumentParser(description='Choose analysis mode and input data')
    parser.add_argument('-m', '--mode',
                        help='mode of analysis: eye, hair, skin',
                        required='True',
                        default='total')
    parser.add_argument('-v', '--vcf',
                        help='genotype data path',
                        required='True')
    parser.add_argument('-p', '--param',
                        help='parameters data path, (default: irisplex-parameters/ directory in repo)',
                        default='irisplex-parameters/')
    parser.add_argument('-s', '--silent',
                        help='on / off -- print the output or not',
                        default='off')
    results = parser.parse_args()

    return (results.mode,
            results.vcf,
            results.param,
            results.silent)


def get_rs(analysis_mode, path_to_param):
    """Get the list of loci relevant for the analysis.

    Relevance of the loci is estimated upon the mode of the analysis.
    The folder that is set by the path contains csv file with the loci list.

    :param analysis_mode: which appearance trait is analysed
    :param path_to_param: where the parameters are stored
    :type analysis_mode: str
    :type path_to_param: str
    :return: list of loci
    :rtype: list
    """
    usepath = os.path.abspath(path_to_param)
    rsnp = []
    for file in os.listdir(usepath):
        # select eye / hair / skin -marks.txt
        if file.startswith(analysis_mode):
            address = os.path.abspath(os.path.join(usepath, file))
            with open(address, 'r', encoding='cp1252') as f:
                for line in f:
                    # exclude comment lines
                    if len(line) > 1 and not line.startswith('#'):
                        line = str.strip(line)
                        rsnp.append(line)
    return rsnp


def _vcf_str_to_lst(vcf_chr_line):
    """Convert line from the vcf file to a list.

    :param vcf_chr_line: line of a vcf file that starts with "chr"
    :type vcf_chr_line: str
    :return: split line of a vcf file
    :rtype: list
    """
    vc_lst = []
    vcf_lst = str.split(vcf_chr_line, sep='\t')
    if len(vcf_lst) == 1:
        vcf_lst = str.split(vcf_lst[0], sep=' ')
    else:
        pass
    for vc_string in vcf_lst:
        if vc_string:
            vc_lst.append(vc_string)
    return vc_lst


def _parse_vcf(file):
    """Select information from the vcf that is required for the analysis.

    :param file: name of the file
    :type file: str
    :return: information on relevant loci
    :rtype: list
    """

    strings = []
    with open(file, 'r', encoding='utf-8') as vicief:
        lab = os.path.basename(file)
        for q, line in enumerate(vicief):
            # exclude comment lines
            if line.startswith('chr'):
                # line is a vcf string that is to become a list
                string = _vcf_str_to_lst(line)
                if string[6] == 'PASS':
                    rs = string[2]
                    if rs != '.':
                        ref = string[3]
                        alt = string[4]
                        gt = str.split(string[9], sep=':')[0]
                        # list containing name of sample, rs,
                        #  reference and alternative nucleotides and genotype
                        lst = [lab, rs, ref, alt, gt]
                        strings.append(lst)
    return strings


def strandcheck(parameters_for_locus):
    """Check which strand snp is in the parameters.

    If needed, change everything to forward strand.

    :param parameters_for_locus: parameters for one locus of IrisPlex model
    :type parameters_for_locus: <class '__main__.Loci'>
    :return: parameters for one locus of IrisPlex model
    """

    complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    if parameters_for_locus.strand == 'R':
        parameters_for_locus.minor_allele = complement[parameters_for_locus.minor_allele]
    return parameters_for_locus


def _value_setter(lst_from_vcf_string, rs_name, beta_parameters):
    """Estimate the genotype.

    According to the parameters of the model, each loci genotype is estimated.

    :param lst_from_vcf_string: data on particular sample from vcf
    :param rs_name: name of the loci that is analysed
    :param beta_parameters: parameters for the model
    :type lst_from_vcf_string: list
    :type rs_name: str
    :type beta_parameters: object
    :return: genotype value (zygosity)
    :rtype: int
    """

    letters = [lst_from_vcf_string[2]]
    gent = str.split(lst_from_vcf_string[4], sep='/')
    alt = str.split(lst_from_vcf_string[3], sep=',')
    for each in alt:
        letters.append(each)
    genotype = [letters[int(gent[0])], letters[int(gent[1])]]
    val = float(0)
    for locus in beta_parameters['loci']:
        loc_param = Loci(locus['name'], locus['minor_allele'],
                         locus['beta1'], locus['beta2'], locus['strand'], locus['rank'])
        if loc_param.name == rs_name:
            loc_param = strandcheck(loc_param)
            for gtype in genotype:
                if gtype == loc_param.minor_allele:
                    val += 1
            return val


def get_snp(vcf_file, snp_list, parameters_dict):
    """ Grep the particular snps relevant for the analysis (from vcf-containing folder)

    :param vcf_file: path to vcf
    :param snp_list: relevant snp
    :param parameters_dict: irisplex parameters
    :type vcf_file: str
    :type snp_list: list
    :type parameters_dict: dict
    :return: values for loci
    :rtype: dict
    """

    bs = {}
    data = _parse_vcf(vcf_file)
    for vcf_string in data:
        for snp in snp_list:
            rs = str.split(vcf_string[1], sep=";")[0]
            # selection of mode-relevant rs
            if snp == rs:
                lab = (vcf_string[0], rs)
                val = _value_setter(vcf_string, rs, parameters_dict)
                bs[lab] = val
    return bs


def param(path_to_param, analysis_mode):
    """ Grep the parameters for a model, parameters is a csv file

    :param path_to_param: where parameters are
    :param analysis_mode: what trait is analysed
    :type path_to_param: str
    :type analysis_mode: str
    :return: irisplex model values
    :rtype: dict
    """
    # path check
    newpath = os.path.abspath(path_to_param)

    for file in os.listdir(newpath):
        name = os.path.join(newpath, file)
        if file.endswith('json') and file.startswith(analysis_mode):
            with open(name, 'r') as inf:
                data = json.load(inf)

    return data


def _sumgetter(lst_beone, lst_betwo):
    """

    :param lst_beone:
    :param lst_betwo:
    :return:
    """
    tot1 = round(sum(lst_beone), 4)
    tot2 = round(sum(lst_betwo), 4)
    sums_lst = [tot1, tot2]
    return sums_lst


def eye_estim(dict_of_analyzed, model_coefficients):
    """

    :param dict_of_analyzed: analysed genotypes
    :param dict_par_for_snp: parameters for IrisPlex
    :return: values for estimation
    """
    # dict_of_analyzed contains genotypes as values and sample name and rs as labels
    # dict_par_for_snp contains beta parameters of IrisPlex model as values
    # and rs as labels
    beone = []
    betwo = []
    for a in dict_of_analyzed:
        rs = str.split(a[1], sep=";")[0]
        for each in model_coefficients['loci']:
            locus = Loci(each['name'], each['minor_allele'], each['beta1'], each['beta2'],
                         each['strand'], each['rank'])
            # match proper parameters
            if rs == locus.name:
                # implement the model
                mf = dict_of_analyzed[a]
                b1 = locus.beta1
                b2 = locus.beta2
                beone.append(mf * b1)
                betwo.append(mf * b2)
    coefs = _sumgetter(beone, betwo)

    return coefs, len(beone)


def hair_estim(dict_of_analyzed, parameters_for_snp):
    """

    :param dict_of_analyzed:
    :param parameters_for_snp:
    :return:
    """
    beone = []
    betwo = []
    betre = []
    for a in dict_of_analyzed:
        rs = str.split(a[1], sep=";")
        for v in parameters_for_snp:
            if rs[0] == v:
                # implement the model
                mf = dict_of_analyzed[a]
                b1 = float((parameters_for_snp[v])[1])
                b2 = float((parameters_for_snp[v])[2])
                b3 = float((parameters_for_snp[v])[3])
                beone.append(mf * b1)
                betwo.append(mf * b2)
                betre.append(mf * b3)
    coefs = [round(sum(beone), 5), round(sum(betwo), 5), round(sum(betre), 5)]
    return coefs, len(beone)


def snp_estim(dict_of_analyzed, model_coefficients, analysis_mode):
    """

    :param dict_of_analyzed:
    :param parameters_for_snp:
    :param analysis_mode:
    :return:
    """
    if analysis_mode == 'eye':
        coefs, loci = eye_estim(dict_of_analyzed, model_coefficients)
    elif analysis_mode == 'hair':
        coefs, loci = hair_estim(dict_of_analyzed, model_coefficients)
    else:
        print("Not available yet.")
        coefs, loci = None
    return coefs, loci


def get_prob(list_w_sums, parameters):
    """

    :param list_w_sums:
    :param parameters:
    :return:
    """
    beta1 = math.exp(float(list_w_sums[0]) + Parameters(parameters).alpha1)
    beta2 = math.exp(float(list_w_sums[1]) + Parameters(parameters).alpha2)
    beta1 = round(beta1, 4)
    beta2 = round(beta2, 4)
    prob = [beta1, beta2]

    return prob


def eyecolor_probs(prob_list):
    """

    :param prob_list:
    :return:
    """
    col = ['blue', 'intermed', 'brown']
    pblue = prob_list[0] / (1 + prob_list[0] + prob_list[1])
    pint = prob_list[1] / (1 + prob_list[0] + prob_list[1])
    pbrown = 1 - pblue - pint
    colors = {col[0]: pblue, col[1]: pint, col[2]: pbrown}

    return colors


def auc_loss(probs, loci, path_to_param, analysis_mode):
    """

    :param probs:
    :param loci:
    :param path_to_param:
    :param analysis_mode:
    :return:
    """
    correction = {}
    newpath = os.path.abspath(path_to_param)
    for file in os.listdir(newpath):
        name = os.path.join(newpath, file)
        if file.endswith('.json') and file.startswith(analysis_mode):
            lab = os.path.splitext(file)[0].split('_')[1]
            if lab == 'accuracy':
                with open(name, 'r') as fp:
                    auc = json.load(fp)
                    for key in auc:
                        correction[key] = (auc[key] - probs[key])

    return correction


def model_iris_plex(snp_sample_dict, model_coefficients, mode_of_analysis, path_to_param):
    """

    :param snp_sample_dict:
    :param beta_coefficients:
    :param mode_of_analysis:
    :param alpha_parameters:
    :return:
    """
    sums, loci = snp_estim(snp_sample_dict, model_coefficients, mode_of_analysis)
    prob = get_prob(sums, model_coefficients)
    # # # Counting three probs
    probs = eyecolor_probs(prob)
    if loci < 6:
        correction = auc_loss(probs, loci, path_to_param, mode_of_analysis)
    else:
        correction = {'blue': 0, 'intermed': 0, 'brown': 0}

    return probs, correction


def verbose_pred_eyes(probability, correction):
    print('Eyes are: ', 'blue', probability['blue'],
          'intermediate', probability['intermed'], 'brown', probability['brown'])
    if all(value == 0 for value in correction.values()):
        pass
    else:
        print('There is loss in AUC according to the missing loci:'
              'for blue:', correction['blue'],
          ', for intermediate:', correction['intermed'], ', for brown:', correction['brown'])


def executable(analysis_mode, vcf_file, path_to_param):
    snip = get_rs(analysis_mode, path_to_param)
    # Read all the parameters
    parameters = param(path_to_param, analysis_mode)
    # selection of snps in a way required for a model
    bs_snp_dict = get_snp(vcf_file, snip, parameters)

    if analysis_mode == 'eye':
        probs, correction = model_iris_plex(bs_snp_dict, parameters, analysis_mode, path_to_param)
        return probs, correction
    elif analysis_mode == 'hair':
        print('Not ready yet!')
        probs = None
        return probs, correction
    else:
        print('This mode is not available')
        probs = None
        return probs, correction


if __name__ == '__main__':
    mode, vcf, par, silent = check_arg()
    if silent == 'off':
        print('mode =', mode)
        print('vcf =', vcf)
        print('param =', par)
        print('silent mode =', silent)
    probabilities, correction = executable(mode, vcf, par)
    if silent == 'off':
        print('You are predicting pigmentation of', mode)

    if silent == 'off':
        if probabilities:
            verbose_pred_eyes(probabilities, correction)