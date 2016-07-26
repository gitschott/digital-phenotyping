import unittest
import model_test
import pandas as pd
from pandas.util.testing import assert_frame_equal


class MT_TestCase(unittest.TestCase):
    """Tests for phenotypic modelling 'model_test.py'"""

    def test_get_rs(self):
        rs_test = ['rs12203592']
        self.assertTrue(model_test.get_rs('iris', '/Users/apple/digital-phenotyping/test_data'), rs_test)

    def test_get_snp(self):
        vcf = '/Users/apple/digital-phenotyping/test_data/test/'
        snp = ['rs6867641']
        bs = {('test','rs6867641'): 0}
        self.assertTrue(model_test.get_snp(vcf, snp), bs)

    def test_snp_estim_eye(self):
        bs = {('BS-test.vcf', 'rs12203592;rs12203592;rs12203592'): 2.0, ('BS-test.vcf', 'rs12896399;rs12896399;rs12896399'): 1.0,\
              ('BS-test.vcf', 'rs16891982;rs16891982;rs16891982'): 2.0, ('BS-test.vcf', 'rs1800407;rs1800407;rs1800407'): 2.0,\
              ('BS-test.vcf', 'rs12913832;rs12913832;rs12913832'): 1.0, ('BS-test.vcf', 'rs1393350;rs1393350;rs1393350'): 2.0}
        beta = {'rs16891982': ['C', '-1.53', '-0.74'], 'rs12913832': ['T', '-4.87', '-1.99'],\
                'rs1800407': ['A', '1.15', '1.05'], 'rs12203592': ['T', '0.60', '0.69'],\
                'rs12896399': ['T', '-0.53', '-0.01'], 'rs1393350': ['A', '0.44', '0.26']}
        res = {'BS-test.vcf': [0.80, 2.45]}
        df = pd.DataFrame(res)
        assert_frame_equal(model_test.snp_estim_eye(bs, beta), df)
    #
    # def test_snp_estim_h4(self):
    #     self.assertTrue(snp_estim_h4(samples, dict_of_analyzed, parameters_for_snp))
    #
    # def test_eyecolor_probs(self):
    #     self.assertTrue(eyecolor_probs(prob_df))



if __name__ == '__main__':
    unittest.main()