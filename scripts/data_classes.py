#!/usr/bin/env python3
from abc import ABC, abstractmethod
from scripts.brent_dekker import brent_dekker
from math import log, sqrt, exp
from scipy.stats import norm


class InputData(ABC):

    def __init__(self, data):
        self.ID = data['ID']
        self.S = float(data['Underlying'])  # spot / future underlying
        self.K = float(data['Strike'])  # strike
        self.r = float(data['Risk-Free Rate'])  # risk-free rate
        self.t = float(data['Days To Expiry'])/365.0  # years to expiry
        self.V0 = float(data['Market Price'])  # market value
        self.underlying_type = data['Underlying Type']
        self.option_type = data['Option Type']
        self.model_type = data['Model Type']
        self.imp_vol = float('nan')  # i.e. sigma => volatility

    def print_input_data(self):
        print('ID:', self.ID, ', spot:', self.S, ', risk-free-interest:', self.r,
              ', time to expiry:', self.t, ', strike:', self.K, ', market value:', self.V0)

    def format_solution(self):
        return [self.ID, self.S, self.K, self.r, self.t, self.option_type, self.model_type, self.imp_vol, self.V0]

    @abstractmethod
    def calc_implied_volatility(self):
        pass


class BlackScholes(InputData):

    # returns d1 and d2, as defined in the black-scholes model
    def stock_probability_factors(self, sigma):
        d1 = (log(self.S / self.K) + (self.r + sigma ** 2 / 2.0) *
              self.t) / (sigma * sqrt(self.t))
        d2 = d1 - sigma * sqrt(self.t)
        return d1, d2

    # finds the implied volatility of a stock option
    def implied_volatility_stock(self):

        if self.option_type == 'Call':
            # trade value as a function of sigma, s.t. f(sigma) = V0, where sigma is the implied volatility
            # returns SN(d1) - Kexp(-rt)N(d2)
            def trade_value_as_func_of_sigma(sigma):
                d1, d2 = self.stock_probability_factors(sigma)
                return self.S * norm.cdf(d1) - self.K * exp(-self.r * self.t) * norm.cdf(d2)

            def trade_value_root(
                sigma): return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        elif self.option_type == 'Put':
            # trade value as a function of sigma, s.t. f(sigma) = V0, where sigma is the implied volatility
            # returns Kexp(-rt)N(-d2) - SN(-d1)
            def trade_value_as_func_of_sigma(sigma):
                d1, d2 = self.stock_probability_factors(sigma)
                return -self.S * norm.cdf(-d1) + self.K * exp(-self.r * self.t) * norm.cdf(-d2)

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 0.01, 0.99)

        else:
            return float('nan')

    # finds the implied volatility of a futures option
    # S is here taken to represent the value of the future underlying, F
    # uses black's model (modified black-scholes), where (essentially) spot price is replaced with a discounted futures price
    # e.g. S <=> F * exp(-r * (T - t))

    # adapted to black-76 method by factoring r out of d1
    def futures_probability_factors(self, sigma):
        d1 = (log(self.S / self.K) + (sigma ** 2 / 2.0) *
              self.t) / (sigma * sqrt(self.t))
        d2 = d1 - sigma * sqrt(self.t)
        return d1, d2

    def implied_volatility_future(self):

        if self.option_type == 'Call':
            # trade value as a function of sigma, such that f(sigma) = V0 where sigma is the implied volatility
            # returns exp(-rt)(SN(d1) - KN(d2))
            def trade_value_as_func_of_sigma(sigma):
                d1, d2 = self.futures_probability_factors(sigma)
                return exp(-self.r * self.t) * (self.S * norm.cdf(d1) - self.K * norm.cdf(d2))

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        elif self.option_type == 'Put':
            # trade value as a function of sigma, such that f(sigma) = V0 where sigma is the implied volatility
            # returns exp(-rt)(KN(-d2) - SN(-d1))
            def trade_value_as_func_of_sigma(sigma):
                d1, d2 = self.futures_probability_factors(sigma)
                return exp(-self.r * self.t) * (self.K * norm.cdf(-d2) - self.S * norm.cdf(-d1))

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        else:
            return float('nan')

    def calc_implied_volatility(self):
        if self.underlying_type == 'Stock':
            self.imp_vol = self.implied_volatility_stock()
        elif self.underlying_type == 'Future':
            self.imp_vol = self.implied_volatility_future()
        else:
            self.imp_vol = float('nan')


# based on the paper 'Option Pricing Model: comparing Louis Bachelier with Black-Scholes Merton', Thomas, 2016 (i),
# the book 'Martingale Methods in Financial Modelling', Musiela et al., 2008 (ii)
class Bachelier(InputData):

    # returns d as from (ii) - eqn. 31a
    # d = d_i / d_ii = (S - Kexp(-rt) / (Kexp(-rt)*sigma*sqrt(t))
    def stock_probability_factor(self, sigma):
        d_i = self.S - self.K * exp(-self.r * self.t)
        d_ii = self.K * exp(-self.r * self.t) * sigma * sqrt(self.t)
        return d_i / d_ii

    def implied_volatility_stock(self):

        if self.option_type == 'Call':
            # trade value as a function of sigma, s.t. f(sigma) = V0, where sigma is the implied volatility
            # returns (S - Kexp(-rt))N(d) + Kexp(-rt)*sigma*sqrt(t)*n(d)
            # where n() represents the probability density of the normal distribution function
            def trade_value_as_func_of_sigma(sigma):
                d = self.stock_probability_factor(sigma)
                K_mod = self.K * exp(-self.r * self.t)  # K_mod = Kexp(-rt)
                return (self.S - K_mod) * norm.cdf(d) + K_mod * sigma * sqrt(self.t) * norm.pdf(d)

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        elif self.option_type == 'Put':
            # trade value as a function of sigma, s.t. f(sigma) = V0, where sigma is the implied volatility
            # returns (S - Kexp(-rt))N(d) + Kexp(-rt)*sigma*sqrt(t)*n(d) + Kexp(-rt) - S
            def trade_value_as_func_of_sigma(sigma):
                d = self.stock_probability_factor(sigma)
                K_mod = self.K * exp(-self.r * self.t)  # K_mod = Kexp(-rt)
                return (self.S - K_mod) * norm.cdf(d) + K_mod * sigma * sqrt(self.t) * norm.pdf(d) + K_mod - self.S

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        else:
            return float('nan')

    # similarly to when using the black-scholes model, to modify the bachelier to accomodate future underlying types,
    # the spot price is replaced with a discounted futures price
    # i.e. S => S * exp(-rt)

    # d = d_i / d_ii = (S - K) / (K*sigma*sqrt(t))
    def futures_probability_factor(self, sigma):
        d_i = self.S - self.K
        d_ii = self.K * sigma * sqrt(self.t)
        return d_i / d_ii

    def implied_volatility_future(self):

        if self.option_type == 'Call':
            # trade value as a function of sigma, s.t. f(sigma) = V0, where sigma is the implied volatility
            # returns (S - K)exp(-rt))N(d) + Kexp(-rt)*sigma*sqrt(t)*n(d)
            def trade_value_as_func_of_sigma(sigma):
                d = self.stock_probability_factor(sigma)
                return (self.S - self.K) * exp(-self.r * self.t) * norm.cdf(d) + self.K * exp(-self.r * self.t) * sigma * sqrt(self.t) * norm.pdf(d)

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        elif self.option_type == 'Put':
            # trade value as a function of sigma, s.t. f(sigma) = V0, where sigma is the implied volatility
            # returns (S - K)exp(-rt)N(d) + Kexp(-rt)*sigma*sqrt(t)*n(d) + Kexp(-rt) - Sexp(-rt)
            def trade_value_as_func_of_sigma(sigma):
                d = self.stock_probability_factor(sigma)
                exp_rt = exp(-self.r * self.t)
                return (self.S - self.K) * exp_rt * norm.cdf(d) + self.K * exp_rt * sigma * sqrt(self.t) * norm.pdf(d) + self.K * exp_rt - self.S * exp_rt

            def trade_value_root(sigma):
                return trade_value_as_func_of_sigma(sigma) - self.V0

            return brent_dekker(trade_value_root, 10 ** -8, 1 - 10 ** -8)

        else:
            return float('nan')

    def calc_implied_volatility(self):
        if self.underlying_type == 'Stock':
            self.imp_vol = self.implied_volatility_stock()
        elif self.underlying_type == 'Future':
            self.imp_vol = self.implied_volatility_future()
        else:
            self.imp_vol = float('nan')


if __name__ == '__main__':

    data1 = {'ID': '23', 'Underlying Type': 'Stock', 'Underlying': '0.8714', 'Risk-Free Rate': '-0.0049', 'Days To Expiry': '211.8715',
             'Strike': '0.9426', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.14370158'}

    data2 = {'ID': '38', 'Underlying Type': 'Stock', 'Underlying': '0.5434', 'Risk-Free Rate': '-0.0045', 'Days To Expiry': '305.1700',
             'Strike': '0.7103', 'Option Type': 'Call', 'Model Type': 'BlackScholes', 'Market Price': '0.09794149'}

    data3 = {'ID': '48', 'Underlying Type': 'Future', 'Underlying': '0.9273', 'Risk-Free Rate': '-0.0020', 'Days To Expiry': '191.2009',
             'Strike': '1.0938', 'Option Type': 'Put', 'Model Type': 'BlackScholes', 'Market Price': '0.2043676'}

    print('bs_stock_put:', BlackScholes(data1).implied_volatility_stock())

    print('bs_stock_call:', BlackScholes(data2).implied_volatility_stock())

    print('bs_future_put:', BlackScholes(data3).implied_volatility_future())
