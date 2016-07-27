#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import poll_parser
import model_test
import argparse


def argu(args=None):
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
    parser.add_argument('-c', '--checklist',
                        help='full path to the tab-delimited phenotypic questionnaire',
                        required='True')
    parser.add_argument('-s', '--sample',
                        help="sample of interest",
                        required='True')
    results = parser.parse_args()
    if results is None:
        print("You need to specify mode of analysis and a path\
         to the vcf file. For detailed information please refer to README")
    return (results.mode,
            results.vcf,
            results.param,
            results.checklist,
            results.sample)


def _eyecolorpred(eyehue_str_list, eye_saturation):
    iris = {' Gray': 2, ' Blue': 1, ' Green': 3,
            ' Hazel': 4, ' Brown': 5, ' I have mixed eye color': 6,
            ' I have heterochromia': 7, ' Red (albino phenotype)': 8}
    eyehue = iris[eyehue_str_list]
    if eyehue < 2:
        prediction = 'Blue'
    elif eyehue > 6:
        prediction = 'Unknown. This is a special case. It is not tested here.'
    elif eyehue == 5:
        prediction = 'Brown'
    elif eyehue == 4:
        if eye_saturation == ' Dark':
            prediction = 'Brown'
        else:
            prediction = 'Intermediate'
    else:
        prediction = 'Intermediate'
    return prediction

if __name__ == '__main__':
    m, v, p, c, s = argu()
    probs = model_test.executable(m, v, p)
    table = poll_parser.whole_poll(c, s)

    print(probs)
    print(table)
