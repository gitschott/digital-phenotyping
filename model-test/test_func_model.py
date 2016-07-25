import unittest
import model_test


class MT_TestCase(unittest.TestCase):
    """Tests for phenotypic modelling 'model_test.py'"""

    def test_get_rs(self):
        rs_test = ['rs12913832', 'rs1800407', 'rs12896399', 'rs16891982', 'rs1393350', 'rs12203592']
        self.assertTrue(model_test.get_rs('eye'), rs_test)

    # def test_mult_all(self):
    #     self.assertTrue(model_test.mult_all(string, file, i))
    #
    # def test_one_all(self):
    #     self.assertTrue(model_test.one_all(string, file, i))
    #
    # def test_get_snp(self):
    #     snp = model_test.get_rs('eye', '/Users/apple/digital-phenotyping/self-report/')
    #     self.assertTrue(model_test.get_snp('/Users/apple/digital-phenotyping/vcf-fold-test/', 'eye'))
    #
    # def test_param(self):
    #     self.assertTrue(model_test.param('/Users/apple/digital-phenotyping/self-report/', 'eye'))
    #
    # def test_grep_snip(self):
    #     beta, alpha = model_test.param ()
    #     self.assertTrue(grep_snip(parameters_for_snp, sample_dictionary))
    #
    # def test_snp_estim_eye(self):
    #     self.assertTrue(estim_eye(samples, dict_of_analyzed, parameters_for_snp))
    #
    # def test_snp_estim_h4(self):
    #     self.assertTrue(snp_estim_h4(samples, dict_of_analyzed, parameters_for_snp))
    #
    # def test_eyecolor_probs(self):
    #     self.assertTrue(eyecolor_probs(prob_df))



if __name__ == '__main__':
    unittest.main()