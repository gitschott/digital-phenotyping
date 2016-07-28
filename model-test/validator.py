#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import poll_parser
import model_test
import argparse
import os


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
                        default='all')
    results = parser.parse_args()
    if results is None:
        print("You need to specify mode of analysis and a path\
         to the vcf file. For detailed information please refer to README")
    return (results.mode,
            results.vcf,
            results.param,
            results.checklist,
            results.sample)


def _pred_count(int, sat):
    if int < 3:
        if sat == ' Dark':
            prediction = 'Intermediate'
        else:
            prediction = 'Blue'
    elif int > 6:
        prediction = 'Unknown. This is a special case. It is not tested here.'
    elif int == 5:
        prediction = 'Brown'
    elif int == 4:
        if sat == ' Dark':
            prediction = 'Brown'
        else:
            prediction = 'Intermediate'
    else:
        prediction = 'Intermediate'
    return prediction

def irisplex_interpreter_poll(poll_parsed_list):
    # greps sample label and eyecolor, modifies it into predicted hue
    predict = []
    for p in poll_parsed_list:
        lab = p[0]
        hue = p[1]
        sat = p[2]
        print(hue)
        iris = {' Gray': 2, ' Blue': 1, ' Green': 3,
                ' Hazel': 4, ' Brown': 5, ' I have mixed eye color': 6,
                ' I have heterochromia': 7, ' Red (albino phenotype)': 8}
        check = type(hue) is list
        if check == True:
            if sat == ' Dark':
                pred = 'Brown'
            else:
                pred = 'Intermediate'
        else:
            pred = _pred_count(iris[hue], sat)
        predict.append([lab, pred])
    return predict


def prob_dict_parser(dict_with_probs):
    print(keys.dict_with_probs)
    pblu = dict_with_probs['blue']
    pint = dict_with_probs['intermed']
    pbro = dict_with_probs['brown']
    if (pblu > pint > pbro) or (pblu > pbro > pint):
        pred = 'blue'

def irisplex_interpreter_model(model_out):
    for i in model_out:
        lab = i[0]
        vals = i[1]

# def verbose_interpreter

if __name__ == '__main__':
    m, v, p, c, s = argu()
    probs = []
    for vc in os.listdir(v):
        if vc.endswith('vcf'):
            filetowork = os.path.join(v, vc)
            prob = model_test.executable(m, filetowork, p, 'off')
            vc = vc[:6]
            res = [vc, prob]
            probs.append(res)

    table, iris_color = poll_parser.whole_poll(c, s)

    pred = irisplex_interpreter_poll(iris_color)
    print(probs)
    
