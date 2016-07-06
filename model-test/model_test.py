import argparse
import sys
import os


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
            os.chdir(path_to_rs_list)
            f = open(file, 'r')
            rs = [line.split('\n') for line in f.readlines()]
            del rs[len(rs) - 1]
            rsnp = []
            for i in rs:
                rsnp.append(i[0])
            del rsnp[len(rsnp) - 1]

            return rsnp

if __name__ == '__main__':
    m, v, p = check_arg(sys.argv[1:])
    print('mode =', m)
    print('vcf =', v)
    print('phen =', p)


    snp = get_rs(m, p)
    if snp == None:
        print('Something whent wrong when we tried to get to rs.')
    else:
        print('You are predicting pigmentation of', m)
        print('Your rs list includes %d elements' % len(snp))