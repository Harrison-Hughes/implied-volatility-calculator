#!/usr/bin/env python3
from abc import ABC, abstractmethod


class InputData(ABC):
    def __init__(self, data):
        self.ID = data['ID']
        self.S = float(data['Underlying'])  # spot price
        self.r = float(data['Risk-Free Rate'])  # risk-free rate
        self.t = float(data['Days To Expiry'])/365.0  # years to expiry
        self.K = float(data['Strike'])  # strike
        self.V0 = float(data['Market Price'])  # market value

    def print_data(self):
        print('ID:', self.ID, ', spot:', self.S, ', risk-free-interest:', self.r,
              ', time to expiry:', self.t, ', strike:', self.K, ', market value:', self.V0)

    @abstractmethod
    def calc_implied_volatility(self):
        pass


class BlackScholes(InputData):
    def calc_implied_volatility(self):
        return('solved')


class Bachelier(InputData):
    def calc_implied_volatility(self):
        return('solved')
