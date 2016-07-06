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

if __name__ == '__main__':
    m, v, p = check_arg(sys.argv[1:])
    print('mode =', m)
    print('vcf =', v)
    print('phen =', p)

    for file in os.listdir(os.path.abspath(p)):
        if file.startswith(m):
            os.chdir(p)
            f = open(file, 'r')
            rs = [line.split('\n') for line in f.readlines()]
            del rs[len(rs)-1]
            print(type(rs))
        else:
            print('wrong phenotyping data path')
