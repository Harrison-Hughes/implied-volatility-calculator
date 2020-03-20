import unittest
from scripts import bd_var_upper_bound as bdub
from math import isclose, sqrt, cos, sin, isnan


class TestBrentDekkerVariableUpperBoundRootFinder(unittest.TestCase):

    def test_inverse_quadratic_interpolation(self):
        self.assertEqual(bdub.inverse_quadratic_interpolation(
            1, 2, 3, -2.365844, 0.362810, 8.435520), 1.8863162489375445)
        with self.assertRaises(ZeroDivisionError):
            bdub.inverse_quadratic_interpolation(1, 2, 3, -2, -2, 0)

    def test_secant_method(self):
        self.assertEqual(bdub.secant_method(1, 2, 3, 4), -2)
        with self.assertRaises(ZeroDivisionError):
            bdub.secant_method(1, 2, 1, 1)

    def test_bisection_method(self):
        self.assertEqual(bdub.bisection_method(-1, 1), 0)
        self.assertEqual(bdub.bisection_method(5, 10), 7.5)

    def test_brent_dekker(self):
        def func1(x): return x**2 - 20  # roots known as +- sqrt(20) ~ +-4.47
        self.assertTrue(isclose(bdub.bd_var_upper_bound(  # pos root
            func1, 4, [5]), sqrt(20)))
        self.assertTrue(isclose(bdub.bd_var_upper_bound(  # neg root
            func1, -4, [-5]), -sqrt(20)))
        self.assertTrue(isnan(bdub.bd_var_upper_bound(  # no root between initial guesses
            func1, -6, [-5])))

        def func2(x): return cos(x) + 2*sin(x) + x**2
        self.assertTrue(
            isclose(bdub.bd_var_upper_bound(func2, -1, [0]), -0.659266046))  # upper root
        self.assertTrue(
            isclose(bdub.bd_var_upper_bound(func2, -1, [-1.5]), -1.271026800))  # lower root
        self.assertTrue(isnan(bdub.bd_var_upper_bound(  # no root between initial guesses
            func1, -2, [0])))
