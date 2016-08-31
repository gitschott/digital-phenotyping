#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import poll_parser
import model_test
import argparse
import os
import json


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
                        help='parameters data path, (default: irisplex-parameters/ directory in repo)',
                        default='irisplex-parameters/')
    parser.add_argument('-c', '--checklist',
                        help='full path to the tab-delimited phenotypic questionnaire',
                        required='True')
    parser.add_argument('-t', '--categories',
                        help="model categories json file",
                        default='irisplex-parameters/poll_param_eye.json')
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
            results.categories,
            results.sample)


def _pred_count(iris_obj, poll_vals):
    if type(poll_vals[iris_obj.hue]) == str:
        prediction = poll_vals[iris_obj.hue]
    else:
        if poll_vals[iris_obj.extra] == poll_vals[iris_obj.hue]:
            if type(poll_vals[iris_obj.extra]) == str:
                prediction = poll_vals[iris_obj.extra]
            else:
                if iris_obj.saturation == ' Dark':
                    prediction = 'Brown'
                else:
                    prediction = 'Intermediate'
        else:
            if iris_obj.saturation == ' Dark':
                prediction = 'Brown'
            else:
                prediction = 'Intermediate'

    return prediction


def irisplex_interpreter_poll(poll_parsed_list, threshold_values):
    # greps sample label and eyecolor, modifies it into predicted hue
    predict = {}
    with open(threshold_values, 'r') as th_v:
        thresh = json.load(th_v)
    for iris in poll_parsed_list:
        pred = _pred_count(iris, thresh)
        predict[iris.name] = pred
    return predict


def iplex_prob_dict_parser(dict_with_probs, model_parameters):
    blue_const = model_parameters["threshold_manual"]["blue"]
    bro_const = model_parameters["threshold_manual"]["brown"]
    pblu = dict_with_probs['blue']
    pint = dict_with_probs['intermed']
    pbro = dict_with_probs['brown']
    if pblu == max(pblu, pint, pbro):
        if pblu >= blue_const:
            pred = 'Blue or Gray'
        else:
            pred = 'Intermediate'
    elif pbro == max(pblu, pint, pbro):
        if pbro > bro_const:
            pred = 'Brown'
        else:
            pred = 'Intermediate'

    else:
        pred = 'Intermediate'
    return pred

def irisplex_interpreter_model(model_out, model_parameters):
    predictions = {}
    corrections = {}
    for i in model_out:
        lab = i[0]
        vals = i[1]
        cor = i[2]
        if all(value == 0 for value in cor.values()):
            mark = False
        else:
            mark = True
        print(lab, vals)
        res = iplex_prob_dict_parser(vals, model_parameters)
        predictions[lab] = res
        corrections[lab] = mark
    return predictions, corrections

def compariser(dct_pred, dct_selfrep, dct_mistakes):
    correct = 0
    wrong = 0
    count = 0
    mistake = []
    for i in dct_selfrep:
        count += 1
        if dct_selfrep[i] == dct_pred[i]:
            correct += 1
            if dct_mistakes[i]:
                print('The result for', i, 'is considered as correct, but it is doubtful, because', i,
                      'sample is lacking loci required for analysis.')
        else:
            wrong += 1
            if dct_mistakes[i]:
                print('The result for', i, 'is considered as wrong, but it is doubtful, because', i,
                      'sample is lacking loci required for analysis.')
            mistake.append(dct_selfrep[i])
            print('It was predicted that', i, 'has eyes coloured', dct_pred[i],
                  'But', i, 'is known for having eyes of', dct_selfrep[i], 'color.')
    return count, correct, wrong, mistake


if __name__ == '__main__':
    mode, vcf, phen_param, checklist, poll_param, s = argu()
    probs = []
    for vc in os.listdir(vcf):
        if vc.endswith('vcf'):
            filetowork = os.path.join(vcf, vc)
            prob, correction = model_test.executable(mode, filetowork, phen_param)
            vc = vc[:6]
            res = [vc, prob, correction]
            probs.append(res)

    parameters = model_test.param(phen_param, mode)
    table, iris_color = poll_parser.whole_poll(checklist, s)
    # pred = irisplex_interpreter_poll(iris_color, poll_thresh)
    pred = irisplex_interpreter_poll(iris_color, poll_param)
    pred_mod, correct_mod = irisplex_interpreter_model(probs, parameters)

    total, yes, no, mistake = compariser(pred_mod, pred, correct_mod)
    print('Prediction is correct in ', float(yes/total)*100, 'per cent cases')
