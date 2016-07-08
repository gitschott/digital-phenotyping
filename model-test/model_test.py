#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import mmap


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
                        help='phenotyping data path',
                        required='True')

    results = parser.parse_args(args)
    return (results.mode,
            results.vcf,
            results.phen)


def get_rs(mode, path_to_rs_list):
    for file in os.listdir(os.path.abspath(p)):
        if file.startswith(mode):
            path = os.getcwd()
            os.chdir(path_to_rs_list)
            f = open(file, 'r')
            rs = [line.split('\n') for line in f.readlines()]
            del rs[len(rs) - 1]
            rsnp = []
            for i in rs:

                rsnp.append(i[0])
            del rsnp[len(rsnp) - 1]
            os.chdir(path)

            return rsnp

if __name__ == '__main__':
    m, v, p = check_arg(sys.argv[1:])
    print('mode =', m)
    print('vcf =', v)
    print('phen =', p)

    snp = get_rs(m, p)

    if snp is None:
        print('Something whent wrong when we tried to get to rs.')
    else:
        print('You are predicting pigmentation of', m)
        print('Your rs list includes %d elements' % len(snp))

    bs = {}

    c = 0
    for file in os.listdir(os.path.abspath(v)):
        path = os.getcwd()
        os.chdir(v)
        vicief = open(file, 'r', encoding='cp1252')
        for q, line in enumerate(vicief):
            if line.startswith('#'):
                pass
            else:
                if line.startswith('chr'):
                    string = str.split(line, sep='\t')
                    for s in string:
                        if s.startswith('rs'):
                            for i in snp:
                                result = re.match(i, s)
                                if result is not None:
                                    if string[6] == 'PASS':
                                        ref = string[3]
                                        if len(string[4]) > 1:
                                            alt = str.split(string[4], sep=',')
                                            af = str.split(string[9], sep=':')
                                            names = str.split(string[8], sep=':')
                                            ind = names.index("AF")
                                            freq = str.split(af[ind], sep=',')
                                            if freq[1:] == freq[:-1]:
                                                bs[file[:6], i] = ref, ref, 0
                                            elif 1 in freq:
                                                ind_f = freq.index(1)
                                                bs[file[:6], i] = alt[ind_f], alt[ind_f], 2
                                            else:
                                                filter(lambda a: a != 0, freq)
                                                print(freq, alt)
                                                f = max(freq)
                                                ind_f = freq.index(f)
                                                print(f, alt[ind_f])
                                                bs[file[:6], i] = ref, alt[ind_f], 1
                                        else:
                                            alt = string[4]
                                            af = str.split(string[9], sep=':')
                                            names = str.split(string[8], sep=':')
                                            ind = names.index("AF")
                                            freq = af[ind]
                                            if freq == 0:
                                                bs[file[:6], i] = ref, ref, 0
                                            elif freq == 1:
                                                bs[file[:6], i] = alt, alt, 2
                                            else:
                                                bs[file[:6], i] = ref, alt, 1
                                    else:
                                        pass
                                else:
                                    pass
        os.chdir(path)
        c += 1


    print(len(bs))
    print(bs)
