import unittest
from scripts import data_classes as dc
from math import isclose, isnan


class TestDataClasses(unittest.TestCase):

    def test_blackscholes_stock_call(self):
        bs_stock_call_data1 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.5434', 'Risk-Free Rate': '-0.0045', 'Days To Expiry': '305.1700',
                               'Strike': '0.7103', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '-0.01'}
        bs_stock_call_data2 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.5434', 'Risk-Free Rate': '-0.0045', 'Days To Expiry': '305.1700',
                               'Strike': '0.7103', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.09794149'}
        bs_stock_call_data3 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.5434', 'Risk-Free Rate': '-0.0045', 'Days To Expiry': '305.1700',
                               'Strike': '0.7103', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.55'}
        # would require sigma < 0
        self.assertTrue(isnan(dc.BlackScholes(
            bs_stock_call_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(
            isclose(dc.BlackScholes(bs_stock_call_data2).implied_volatility_stock(), 0.758711204696251))
        # would require sigma > 1000, which is above the given limit
        self.assertTrue(isnan(dc.BlackScholes(
            bs_stock_call_data3).implied_volatility_stock()))

    def test_blackscholes_stock_put(self):
        bs_stock_put_data1 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                              'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.0370158'}
        bs_stock_put_data2 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                              'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.14370158'}
        bs_stock_put_data3 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                              'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.95'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(dc.BlackScholes(
            bs_stock_put_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(dc.BlackScholes(
            bs_stock_put_data2).implied_volatility_stock(), 0.37290063720593675))
        # would require sigma > 1000, which is above the given limit
        self.assertTrue(isnan(dc.BlackScholes(
            bs_stock_put_data3).implied_volatility_stock()))

    def test_blackscholes_future_call(self):
        pass
