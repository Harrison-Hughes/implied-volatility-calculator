import unittest
from scripts import trade_classes as tc
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
        self.assertTrue(isnan(tc.BlackScholes(
            bs_stock_call_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(
            isclose(tc.BlackScholes(bs_stock_call_data2).implied_volatility_stock(), 0.758711204696251))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bs_stock_call_data3).implied_volatility_stock()))

    def test_blackscholes_stock_put(self):
        bs_stock_put_data1 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                              'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.0370158'}
        bs_stock_put_data2 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                              'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.14370158'}
        bs_stock_put_data3 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
                              'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.95'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bs_stock_put_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.BlackScholes(
            bs_stock_put_data2).implied_volatility_stock(), 0.37290063720593675))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bs_stock_put_data3).implied_volatility_stock()))

    def test_blackscholes_future_call(self):
        bs_future_call_data1 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.3315', 'Risk-Free Rate': '-0.0007', 'Days To Expiry': '377.3859',
                                'Strike': '1.4348', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '-0.01'}
        bs_future_call_data2 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.3315', 'Risk-Free Rate': '-0.0007', 'Days To Expiry': '377.3859',
                                'Strike': '1.4348', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.21010422'}
        bs_future_call_data3 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.3315', 'Risk-Free Rate': '-0.0007', 'Days To Expiry': '377.3859',
                                'Strike': '1.4348', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '1.35'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bs_future_call_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.BlackScholes(
            bs_future_call_data2).implied_volatility_stock(), 0.46585749989521125))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bs_future_call_data3).implied_volatility_stock()))

    def test_blackscholes_future_put(self):
        bs_future_put_data1 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '0.1855', 'Risk-Free Rate': '-0.0000', 'Days To Expiry': '279.5115',
                               'Strike': '0.2021', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.000103566'}
        bs_future_put_data2 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '0.1855', 'Risk-Free Rate': '-0.0000', 'Days To Expiry': '279.5115',
                               'Strike': '0.2021', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.050103566'}
        bs_future_put_data3 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '0.1855', 'Risk-Free Rate': '-0.0000', 'Days To Expiry': '279.5115',
                               'Strike': '0.2021', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.250103566'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bs_future_put_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.BlackScholes(
            bs_future_put_data2).implied_volatility_stock(), 0.6178494422980207))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bs_future_put_data3).implied_volatility_stock()))

    def test_bachelier_stock_call(self):
        bac_stock_call_data1 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '1.1975', 'Risk-Free Rate': '-0.0023', 'Days To Expiry': '190.1082',
                                'Strike': '1.4481', 'Option Type': 'Call', 'Model Type': 'Bachelier', 'Market Price': '-0.01'}
        bac_stock_call_data2 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '1.1975', 'Risk-Free Rate': '-0.0023', 'Days To Expiry': '190.1082',
                                'Strike': '1.4481', 'Option Type': 'Call', 'Model Type': 'Bachelier', 'Market Price': '0.3641165'}
        bac_stock_call_data3 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '1.1975', 'Risk-Free Rate': '-0.0023', 'Days To Expiry': '190.1082',
                                'Strike': '1.4481', 'Option Type': 'Call', 'Model Type': 'Bachelier', 'Market Price': '1.2641165'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bac_stock_call_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.Bachelier(
            bac_stock_call_data2).implied_volatility_stock(), 1.1493242378562218))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bac_stock_call_data3).implied_volatility_stock()))

    def test_bachelier_stock_put(self):
        bac_stock_put_data1 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '1.5853', 'Risk-Free Rate': '-0.0003', 'Days To Expiry': '336.6476',
                               'Strike': '1.8868', 'Option Type': 'Put', 'Model Type': 'Bachelier', 'Market Price': '0.1068661'}
        bac_stock_put_data2 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '1.5853', 'Risk-Free Rate': '-0.0003', 'Days To Expiry': '336.6476',
                               'Strike': '1.8868', 'Option Type': 'Put', 'Model Type': 'Bachelier', 'Market Price': '0.6068661'}
        bac_stock_put_data3 = {'ID': '0', 'Underlying Type': 'Stock', 'Underlying': '1.5853', 'Risk-Free Rate': '-0.0003', 'Days To Expiry': '336.6476',
                               'Strike': '1.8868', 'Option Type': 'Put', 'Model Type': 'Bachelier', 'Market Price': '2.0'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bac_stock_put_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.Bachelier(
            bac_stock_put_data2).implied_volatility_stock(), 0.6077171262336497))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bac_stock_put_data3).implied_volatility_stock()))

    def test_bachelier_future_call(self):
        bac_future_call_data1 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.4597', 'Risk-Free Rate': '-0.0002', 'Days To Expiry': '65.8745',
                                 'Strike': '1.4992', 'Option Type': 'Call', 'Model Type': 'Bachelier', 'Market Price': '-0.01'}
        bac_future_call_data2 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.4597', 'Risk-Free Rate': '-0.0002', 'Days To Expiry': '65.8745',
                                 'Strike': '1.4992', 'Option Type': 'Call', 'Model Type': 'Bachelier', 'Market Price': '0.049442439'}
        bac_future_call_data3 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.4597', 'Risk-Free Rate': '-0.0002', 'Days To Expiry': '65.8745',
                                 'Strike': '1.4992', 'Option Type': 'Call', 'Model Type': 'Bachelier', 'Market Price': '1.549442439'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bac_future_call_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.Bachelier(
            bac_future_call_data2).implied_volatility_stock(), 0.2651761392457692))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bac_future_call_data3).implied_volatility_stock()))

    def test_bachelier_future_put(self):
        bac_future_put_data1 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.8360', 'Risk-Free Rate': '-0.0031', 'Days To Expiry': '242.7474',
                                'Strike': '2.2491', 'Option Type': 'Put', 'Model Type': 'Bachelier', 'Market Price': '0.24574876'}
        bac_future_put_data2 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.8360', 'Risk-Free Rate': '-0.0031', 'Days To Expiry': '242.7474',
                                'Strike': '2.2491', 'Option Type': 'Put', 'Model Type': 'Bachelier', 'Market Price': '0.74574876'}
        bac_future_put_data3 = {'ID': '0', 'Underlying Type': 'Future', 'Underlying': '1.8360', 'Risk-Free Rate': '-0.0031', 'Days To Expiry': '242.7474',
                                'Strike': '2.2491', 'Option Type': 'Put', 'Model Type': 'Bachelier', 'Market Price': '2.74574876'}
        # no sigma exists to satisfy equation
        self.assertTrue(isnan(tc.BlackScholes(
            bac_future_put_data1).implied_volatility_stock()))
        # sigma exists
        self.assertTrue(isclose(tc.Bachelier(
            bac_future_put_data2).implied_volatility_stock(), 0.69538421132548))
        # would require sigma > 1000, which is above the limit that I chose
        self.assertTrue(isnan(tc.BlackScholes(
            bac_future_put_data3).implied_volatility_stock()))
