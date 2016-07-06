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


def boyermoorehorspool(pattern, text):
    m = len(pattern)
    n = len(text)
    if m > n: return -1
    skip = []
    for k in range(256): skip.append(m)
    print(skip)
    for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
    skip = tuple(skip)
    k = m - 1
    while k < n:
        j = m - 1; i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1; i -= 1
        if j == -1: return i + 1
        k += skip[ord(text[k])]
    return -1

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
        with open(file, 'r', encoding='cp1252') as vicief:
            for q, line in enumerate(vicief):
                for i in snp:
                    text = line
                    pattern = i
                    s = boyermoorehorspool(pattern, text)
                    print('Text:', text)
                    print('Pattern:', pattern)
                    if s > -1:
                        print('Pattern' + pattern + 'found at position', s )

                        # bs["{0}".format(i)] = re.match(i, line)
        os.chdir(path)
        c += 1
            # for line in vicief:
            #     for i in snp:
            #        if 'i' in line:
            #            print(i, line)
        # with open(file, 'rb', 0) as tex, \
        #         mmap.mmap(tex.fileno(), 0, access=mmap.ACCESS_READ) as s:
        #     for i in snp:
        #        if s.find(b'i') != -1:
        #            print(s)

        # f = open(file, mode='rt', encoding='cp1252')
        # for q, line in enumerate(f):
        #    for i in snp:
        #         bs["{0}".format(i)] = re.match(i, line)
        # print(answer)
    print(bs)
    print(c)
    print(snp)
