import unittest
import argparse
import os
import model_test


class MT_TestCase(unittest.TestCase):
    """Tests for phenotypic modelling 'model_test.py'"""

    def test_get_rs(self):
        rs_test = ['rs12913832', 'rs1800407', 'rs12896399', 'rs16891982', 'rs1393350', 'rs12203592']
        self.assertTrue(model_test.get_rs('iris', 'test_data/'), rs_test)

    def test_parse_vcf(self):
        parse_test = [['chr5', '33985857', 'rs6867641;rs6867641;rs6867641', 'T', 'A,C,G', '659.28', 'PASS',\
                       'AF=0,0,0;AO=0,1,0;DP=1471;FAO=0,0,0;FDP=1470;FR=.,REALIGNEDx0.01291;FRO=1470;\
                       FSAF=0,0,0;FSAR=0,0,0;FSRF=802;FSRR=668;FWDB=-0.0328621,-0.0979912,-0.0366488;FXX=0.00135869;\
                       HRUN=1,1,1;HS;LEN=1,1,1;MLLD=295.99,92.4138,112.378;QD=1.79396;RBI=0.0328856,0.0990347,0.0407483;\
                       REFB=-2.56444e-06,-5.66972e-05,-2.38632e-05;REVB=-0.00124371,-0.0143383,-0.0178126;RO=1467;\
                       SAF=0,1,0;SAR=0,0,0;SRF=802;SRR=665;SSEN=0,0,0;SSEP=0,0,0;SSSB=0,0.0133506,0;STB=0.5,0.5,0.5;\
                       STBP=1,1,1;TYPE=snp,snp,snp;VARB=0,0,0;OID=rs6867641,rs6867641,rs6867641;OPOS=33985857,33985857,33985857;\
                       OREF=T,T,T;OALT=A,C,G;OMAPALT=A,C,G', 'GT:GQ:DP:FDP:RO:FRO:AO:FAO:AF:SAR:SAF:SRF:SRR:FSAR:FSAF:FSRF:FSRR',\
                       '0/0:99:1471:1470:1467:1470:0,1,0:0,0,0:0,0,0:0,0,0:0,1,0:802:665:0,0,0:0,0,0:802:668'], ['chr7',\
                       '18890000', 'rs756853;rs756853;rs756853', 'G', 'A,C,T', '3368.51', 'PASS', 'AF=0.521327,0,0;AO=769,0,1;\
                       DP=1478;FAO=770,0,0;FDP=1477;FR=.,REALIGNEDx0.5236;FRO=707;FSAF=405,0,0;FSAR=365,0,0;FSRF=347;FSRR=360;\
                       FWDB=-0.0253494,-0.0361379,-0.0524978;FXX=0.00202701;HRUN=1,1,1;HS;LEN=1,1,1;MLLD=344.237,99.9132,76.2571;\
                       QD=9.12256;RBI=0.0304883,0.0525321,0.0658507;REFB=-0.0134517,0.0113744,0.018087;REVB=0.0169394,0.038127,0.039753;\
                       RO=705;SAF=405,0,0;SAR=364,0,1;SRF=347;SRR=358;SSEN=0,0,0;SSEP=0,0,0;SSSB=0.0303228,0,-0.0290067;\
                       STB=0.516849,0.5,0.5;STBP=0.204,1,1;TYPE=snp,snp,snp;VARB=0.0125481,0,0;OID=rs756853,rs756853,rs756853;\
                       OPOS=18890000,18890000,18890000;OREF=G,G,G;OALT=A,C,T;OMAPALT=A,C,T',\
                       'GT:GQ:DP:FDP:RO:FRO:AO:FAO:AF:SAR:SAF:SRF:SRR:FSAR:FSAF:FSRF:FSRR',\
                       '0/1:99:1478:1477:705:707:769,0,1:770,0,0:0.521327,0,0:364,0,1:405,0,0:347:358:365,0,0:405,0,0:347:360']
        list = os.listdir(v)
        self.assertTrue(model_test.parse_vcf(v))
        self.assertFalse(model_test.parse_vcf(p), msg='The folder is not correct!')

    def test_mult_all(self):
        self.assertTrue(model_test.mult_all(string, file, i))

    def test_one_all(self):
        self.assertTrue(model_test.one_all(string, file, i))

    def test_get_snp(self):
        snp = model_test.get_rs('eye', '/Users/apple/digital-phenotyping/self-report/')
        self.assertTrue(model_test.get_snp('/Users/apple/digital-phenotyping/vcf-fold-test/', 'eye'))
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