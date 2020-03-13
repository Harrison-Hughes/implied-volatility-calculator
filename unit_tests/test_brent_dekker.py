import unittest
from scripts import brent_dekker as bd
from math import isclose, sqrt, cos, sin, isnan

print(bd.__file__)


class TestBrentDekkerRootFinder(unittest.TestCase):

    def test_inverse_quadratic_interpolation(self):
        self.assertEqual(bd.inverse_quadratic_interpolation(
            1, 2, 3, -2.365844, 0.362810, 8.435520), 1.8863162489375445)
        with self.assertRaises(ZeroDivisionError):
            bd.inverse_quadratic_interpolation(1, 2, 3, -2, -2, 0)

    def test_secant_method(self):
        self.assertEqual(bd.secant_method(1, 2, 3, 4), -2)
        with self.assertRaises(ZeroDivisionError):
            bd.secant_method(1, 2, 1, 1)

    def test_bisection_method(self):
        self.assertEqual(bd.bisection_method(-1, 1), 0)
        self.assertEqual(bd.bisection_method(5, 10), 7.5)

    def test_brent_dekker(self):
        def func1(x): return x**2 - 20  # roots known as +- sqrt(20) ~ +-4.47
        self.assertTrue(isclose(bd.brent_dekker(
            func1, 4, 5)[0], sqrt(20)))
        self.assertTrue(isclose(bd.brent_dekker(
            func1, 5, 4)[0], sqrt(20)))
        self.assertTrue(isclose(bd.brent_dekker(
            func1, -4, -5)[0], -1*sqrt(20)))
        self.assertTrue(isnan(bd.brent_dekker(
            func1, -6, -5)[0]))

        def func2(x): return cos(x) + 2*sin(x) + x**2
        self.assertTrue(
            isclose(bd.brent_dekker(func2, 0, -1)[0], -0.659266046))
        self.assertTrue(
            isclose(bd.brent_dekker(func2, -2, -1)[0], -1.271026800))
        self.assertTrue(isnan(bd.brent_dekker(
            func1, -2, 0)[0]))


if __name__ == "__main__":
    unittest.main
