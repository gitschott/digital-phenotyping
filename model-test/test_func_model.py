import unittest
import model_test


class MT_TestCase(unittest.TestCase):
    """Tests for phenotypic modelling 'model_test.py'"""

    def test_check_arg(self):
        """Are arguments parsed correctly?"""
        self.assertTrue(model_test.check_arg(args=None))

    def test_get_rs(self):
        self.assertTrue(model_test.get_rs(m, p))
        self.assertFalse(model_test.get_rs(m, v), msg='The folder is not correct!')

    def test_parse_vcf(self):
        self.assertTrue(model_test.parse_vcf(v))
        self.assertFalse(model_test.parse_vcf(p), msg='The folder is not correct!')

    def test_mult_all(self):
        self.assertTrue(mult_all(string, file, i))
    #
    # def test_one_all(self):
    #     self.assertTrue(one_all(string, file, i))

    def test_get_snp(self):
        snp = model_test.get_rs(m, p)
        self.assertTrue(model_test.get_snp(v, m))

    def test_param(self):
        self.assertTrue(param(p, m))

    # def test_grep_snip(self):
    #     beta, alpha = param ()
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