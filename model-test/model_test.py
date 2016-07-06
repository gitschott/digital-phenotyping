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


# Generate the Bad Character Skip List
def generate_bad_char_shift(term):
    skipList = {}
    for i in range(0, len(term) - 1):
        skipList[term[i]] = len(term) - i - 1
    return skipList


# Generate the Good Suffix Skip List
def findSuffixPosition(badchar, suffix, full_term):
    for offset in range(1, len(full_term) + 1)[::-1]:
        flag = True
        for suffix_index in range(0, len(suffix)):
            term_index = offset - len(suffix) - 1 + suffix_index
            if term_index < 0 or suffix[suffix_index] == full_term[term_index]:
                pass
            else:
                flag = False
        term_index = offset - len(suffix) - 1
        if flag and (term_index <= 0 or full_term[term_index - 1] != badchar):
            return len(full_term) - offset + 1


def generateSuffixShift(key):
    skipList = {}
    buffer = ""
    for i in range(0, len(key)):
        skipList[len(buffer)] = findSuffixPosition(key[len(key) - 1 - i], buffer, key)
        buffer = key[len(key) - 1 - i] + buffer
    return skipList


# Actual Search Algorithm
def BMSearch(haystack, needle):
    goodSuffix = generateSuffixShift(needle)
    badChar = generate_bad_char_shift(needle)
    i = 0
    while i < len(haystack) - len(needle) + 1:
        j = len(needle)
        while j > 0 and needle[j - 1] == haystack[i + j - 1]:
            j -= 1
        if j > 0:
            badCharShift = badChar.get(haystack[i + j - 1], len(needle))
            goodSuffixShift = goodSuffix[len(needle) - j]
            if badCharShift > goodSuffixShift:
                i += badCharShift
            else:
                i += goodSuffixShift
        else:
            return i
    return -1

    while k < n:
        j = m - 1
        i = k
        while j >= 0 and text[i] == pattern[j]:
            j -= 1
            i -= 1
        if j == -1:
            return i + 1
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
        vicief = open(file, 'r', encoding='cp1252')
        for q, line in enumerate(vicief):
            for i in snp:
                print(line)
                print(i)
                bs["{0}".format(i)] = BMSearch(line, i)
        os.chdir(path)
        c += 1

    print(bs)
    print(c)
    print(snp)
