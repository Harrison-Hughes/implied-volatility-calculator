#!/usr/bin/env python3
from abc import ABC, abstractmethod
from math import log, sqrt


class InputData(ABC):

    def __init__(self, data):
        self.ID = data['ID']
        self.S = float(data['Underlying'])  # spot
        self.K = float(data['Strike'])  # strike
        self.r = float(data['Risk-Free Rate'])  # risk-free rate
        self.t = float(data['Days To Expiry'])/365.0  # years to expiry
        self.V0 = float(data['Market Price'])  # market value
        self.underlying_type = data['Underlying Type']
        self.option_type = data['Option Type']

    def print_data(self):
        print('ID:', self.ID, ', spot:', self.S, ', risk-free-interest:', self.r,
              ', time to expiry:', self.t, ', strike:', self.K, ', market value:', self.V0)

    @abstractmethod
    def calc_implied_volatility(self):
        pass


class BlackScholes(InputData):

    def probability_factors(self, sigma):
        d1 = (log(self.S/self.K)+(self.r+sigma**2/2.0) *
              self.t)/(sigma*sqrt(self.t))
        d2 = d1 - sigma*sqrt(self.t)
        return d1, d2

    def imp_vol_stock(self, sigma, option_type):
        # d1, d2 = probability_factors(self, sigma)
        pass

    def imp_vol_future(self, sigma, option_type):
        # d1, d2 = probability_factors(self, sigma)
        pass

    def calc_implied_volatility(self):
        return('solved')


class Bachelier(InputData):

    def probability_factor(self, sigma):
        pass

    def calc_implied_volatility(self):
        return('solved')
