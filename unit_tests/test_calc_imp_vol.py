import unittest
from scripts import data_classes as dc
from math import isclose, isnan


class TestDataClasses(unittest.TestCase):

    def test_blackscholes_stock_call(self):
        call_data1 = {'ID': '23', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                      'Strike': '0.9426', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.14370158'}
        call_data2 = {'ID': '38', 'Underlying Type': 'Stock', 'Underlying': '0.5434', 'Risk-Free Rate': '-0.0045', 'Days To Expiry': '305.1700',
                      'Strike': '0.7103', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.09794149'}
        call_data3 = {'ID': '23', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                      'Strike': '0.9426', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.14370158'}
        # would require sigma < 0
        self.assertTrue(isnan(dc.BlackScholes(
            call_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(
            isclose(dc.BlackScholes(call_data2), 0.758711204696251))
        # would require sigma > 1
        self.assertTrue(isnan(dc.BlackScholes(
            call_data3).implied_volatility_stock()))

    def test_blackscholes_stock_out(self):
        put_data = {'ID': '23', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                    'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.14370158'}
        self.assertEqual(dc.BlackScholes(
            put_data).implied_volatility_stock(), 0)
