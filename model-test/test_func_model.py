#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import model_test


class MT_TestCase(unittest.TestCase):
    """Tests for phenotypic modelling 'model_test.py'"""

    def test_get_rs(self):
        rs_test = ['rs12203592']
        self.assertEqual(model_test.get_rs('iris', '/Users/apple/digital-phenotyping/test_data'), rs_test)

    def test__parse_vcf(self):
        vcf = '/Users/apple/digital-phenotyping/test_data/test/BS-tst.vcf'
        strings = [['BS-tst.vcf', 'rs6867641;rs6867641;rs6867641', 'T', 'A,C,G', '0/0' ],
                   ['BS-tst.vcf', 'rs756853;rs756853;rs756853', 'G', 'A,C,T', '0/1']]
        self.assertEqual(model_test._parse_vcf(vcf), strings)

    # def test__value_setter(self):

    def test_get_snp(self):
        vcf = '/Users/apple/digital-phenotyping/test_data/test/BS-tst.vcf'
        snp = ['rs6867641']
        bs = {('BS-tst.vcf','rs6867641'): 0.0}
        self.assertEqual(model_test.get_snp(vcf, snp), bs)

    def test_eye_estim(self):
        bs = {('BS-test.vcf', 'rs12203592;rs12203592;rs12203592'): 2.0, ('BS-test.vcf', 'rs12896399;rs12896399;rs12896399'): 1.0,\
              ('BS-test.vcf', 'rs16891982;rs16891982;rs16891982'): 2.0, ('BS-test.vcf', 'rs1800407;rs1800407;rs1800407'): 2.0,\
              ('BS-test.vcf', 'rs12913832;rs12913832;rs12913832'): 1.0, ('BS-test.vcf', 'rs1393350;rs1393350;rs1393350'): 2.0}
        beta = {'rs16891982': ['C', '-1.53', '-0.74'], 'rs12913832': ['T', '-4.87', '-1.99'],\
                'rs1800407': ['A', '1.15', '1.05'], 'rs12203592': ['T', '0.60', '0.69'],\
                'rs12896399': ['T', '-0.53', '-0.01'], 'rs1393350': ['A', '0.44', '0.26']}
        res = [-4.08, 0.52]
        self.assertEqual(model_test.eye_estim(bs, beta), res)

    def test__sumgetter(self):
        l1 = [2.3, 1.2, 0.44, -4.87, -0.0, -1.06]
        l2 = [2.1, 1.38, 0.26, -1.99, -0.0, -0.02]
        strings = [-1.37, 1.49]
        self.assertEqual(model_test._sumgetter(l1, l2), strings)

    def test_get_prob(self):
        sums = [1, 1]
        alpha = [['3.84', '0.37']]
        res = [126.4694, 3.9354]
        self.assertEqual(model_test.get_prob(sums, alpha), res)

    def eyecolor_prob(self):
        list = [1, 6]
        res = {'blue': 0.125, 'intermed': 0.75, 'brown': 0.125}
        self.assertEqual(model_test.eyecolor_probs(list), res)



if __name__ == '__main__':
    unittest.main()