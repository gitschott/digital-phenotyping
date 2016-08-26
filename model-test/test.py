import unittest
import model_test

class MTCase(unittest.TestCase):
    """Tests for prediction model"""


    def test_get_rs(self):
        rs_list_eye = ['rs7495174', 'rs4778138', 'rs1800407', 'rs1800401', 'rs916977', 'rs1129038', 'rs12913832',
                       'rs2228479', 'rs1805007', 'rs1805008', 'rs12896399', 'rs16891982', 'rs26722', 'rs1426654',
                       'rs1724630', 'rs2733832', 'rs1042602', 'rs1393350', 'rs12203592']
        rs_list_hair = ['rs1408799', 'rs1805005', 'rs1805006', 'rs2228479', 'rs11547464', 'rs1805007', 'rs1110400',
                        'rs1805008', 'rs885479', 'rs1805009', 'rs1015362', 'rs4911414', 'rs12821256', 'rs35264875',
                        'rs3829241', 'rs683', 'N29insA', 'Y152OCH', 'rs1800407', 'rs12913832', 'rs16891982',
                        'rs12203592', 'rs12896399', 'rs1393350']
        self.assertEqual(model_test.get_rs('eye', '/Users/apple/digital-phenotyping/self-report/'), rs_list_eye)
        self.assertEqual(model_test.get_rs('hair', '/Users/apple/digital-phenotyping/self-report/'), rs_list_hair)
        self.assertNotEqual(model_test.get_rs('eye', '/Users/apple/digital-phenotyping/vcf-fold-test/'), msg='The folder is not correct!')

if __name__ == '__main__':
    unittest.main()