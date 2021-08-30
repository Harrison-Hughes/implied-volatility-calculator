import unittest
import trade_classes as tc
import bd_var_bounds as bdvb
from math import isclose, sqrt, cos, sin, isnan


class TestBrentDekkerVariableBoundsRootFinder(unittest.TestCase):

    def test_inverse_quadratic_interpolation(self):
        self.assertEqual(bdvb.inverse_quadratic_interpolation(
            1, 2, 3, -2.365844, 0.362810, 8.435520), 1.8863162489375445)
        with self.assertRaises(ZeroDivisionError):
            bdvb.inverse_quadratic_interpolation(1, 2, 3, -2, -2, 0)

    def test_secant_method(self):
        self.assertEqual(bdvb.secant_method(1, 2, 3, 4), -2)
        with self.assertRaises(ZeroDivisionError):
            bdvb.secant_method(1, 2, 1, 1)

    def test_bisection_method(self):
        self.assertEqual(bdvb.bisection_method(-1, 1), 0)
        self.assertEqual(bdvb.bisection_method(5, 10), 7.5)

    def test_brent_dekker_var_bounds(self):
        def func1(x): return x**2 - 20  # roots known as +- sqrt(20) ~ +-4.47
        self.assertTrue(isclose(bdvb.bd_var_bounds(  # pos root
            func1, [4, 5]), sqrt(20)))
        self.assertTrue(isclose(bdvb.bd_var_bounds(  # neg root
            func1, [-4, -5]), -sqrt(20)))
        self.assertTrue(isnan(bdvb.bd_var_bounds(  # no root between initial guesses
            func1, [2, 3])))
        self.assertTrue(isclose(bdvb.bd_var_bounds(  # if no root between initial guesses, finds between subsequent
            func1, [3, 4, 5]), sqrt(20)))

        def func2(x): return cos(x) + 2*sin(x) + x**2
        self.assertTrue(
            isclose(bdvb.bd_var_bounds(func2, [-1, 0]), -0.659266046))  # upper root
        self.assertTrue(
            isclose(bdvb.bd_var_bounds(func2, [-1, -1.5]), -1.271026800))  # lower root
        self.assertTrue(isnan(bdvb.bd_var_bounds(  # no root between given bounds
            func1, [-2, 0])))


class TestTradeClasses(unittest.TestCase):

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
