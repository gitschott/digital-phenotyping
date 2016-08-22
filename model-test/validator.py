#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import poll_parser
import model_test
import argparse
import os
import csv


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
    parser.add_argument('-t', '--threshold',
                        help="model output categories csv file, default: self-report/iris_thresh.csv",
                        required='True')
    parser.add_argument('-cat', '--categories',
                        help="model categories csv file",
                        default=0.65)
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
            results.threshold,
            results.categories,
            results.sample)


def _pred_count(int, sat):
    if int < 3:
        prediction = 'Blue or Gray'
        # if sat == ' Dark':
        #     prediction = 'Intermediate'
        # else:
        #     prediction = 'Blue'
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

def irisplex_interpreter_poll(poll_parsed_list, threshold_csv):
    print(poll_parsed_list, threshold_csv)
    # greps sample label and eyecolor, modifies it into predicted hue
    predict = {}
    iris = {}
    with open(threshold_csv, encoding='utf-8') as csvfile:
        iris_thresh = csv.reader(csvfile, delimiter=';')
        for row in iris_thresh:
            iris[row[0]] = int(row[1])
    for p in poll_parsed_list:
        lab = p[0]
        hue = p[1]
        sat = p[2]
        check = type(hue) is list
        print(lab, hue, sat)
        # if check == True:
        #     if sat == ' Dark':
        #         pred = 'Brown'
        #     else:
        #         pred = 'Intermediate'
        # else:
        pred = _pred_count(iris[hue], sat)
        predict[lab] = pred
    return predict


def iplex_prob_dict_parser(dict_with_probs, threshold_csv):
    with open(threshold_csv, encoding='utf-8') as csvfile:
        iris_thresh = csv.reader(csvfile, delimiter=';')
        _ = next(iris_thresh)
        for row in iris_thresh:
            blue_const = float(row[0])
            bro_const = float(row[0])
    pblu = dict_with_probs['blue']
    pint = dict_with_probs['intermed']
    pbro = dict_with_probs['brown']
    if (pblu > pint > pbro) or (pblu > pbro > pint):
        if pblu < blue_const:
            pred = 'Intermediate'
        else:
            pred = 'Blue or Gray'
    elif (pbro > pint > pblu) or (pbro > pblu > pint):
        if pbro > bro_const:
            pred = 'Brown'
        else:
            pred = 'Intermediate'

    else:
        pred = 'Intermediate'
    return pred

def irisplex_interpreter_model(model_out, threshold_csv):
    predictions = {}
    for i in model_out:
        lab = i[0]
        vals = i[1]
        res = iplex_prob_dict_parser(vals, threshold_csv)
        predictions[lab] = res
    return predictions

def compariser(dct_pred, dct_selfrep):
    correct = 0
    wrong = 0
    count = 0
    mistake = []
    for i in dct_selfrep:
        count +=1
        if dct_selfrep[i] == dct_pred[i]:
            correct +=1
        else:
            wrong +=1
            mistake.append(dct_selfrep[i])
            print('It was predicted that', i, 'has eyes coloured', dct_pred[i],
                  'But', i, 'is known for having eyes of', dct_selfrep[i], 'color.')
    return count, correct, wrong, mistake


if __name__ == '__main__':
    mode, vcf, phen_param, checklist, thresh, poll_thresh, s = argu()
    probs = []
    for vc in os.listdir(vcf):
        if vc.endswith('vcf'):
            filetowork = os.path.join(vcf, vc)
            prob = model_test.executable(mode, filetowork, phen_param)
            vc = vc[:6]
            res = [vc, prob]
            probs.append(res)

    table, iris_color = poll_parser.whole_poll(checklist, s)

    pred = irisplex_interpreter_poll(iris_color, poll_thresh)
    pred_mod = irisplex_interpreter_model(probs, thresh)

    total, yes, no, mistake = compariser(pred_mod, pred)
    print('Model is correct in ', float(yes/total)*100, 'per cent cases')
