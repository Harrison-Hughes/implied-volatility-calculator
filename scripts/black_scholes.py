#!/usr/bin/env python3
from scipy.stats import norm
from math import sqrt, exp, log, pi


def d(sigma, S, K, r, t):
    d1 = 1 / (sigma * sqrt(t)) * (log(S/K) + (r + sigma**2/2) * t)
    d2 = d1 - sigma * sqrt(t)
    return d1, d2


def call_price(sigma, S, K, r, t, d1, d2):
    C = norm.cdf(d1) * S - norm.cdf(d2) * K * exp(-r * t)
    return C


def put_price(sigma, S, K, r, t, d1, d2):
    C = K * norm.cdf(d2 * -1) * exp(-r * t) - S * norm.cdf(d1 * -1)
    return C


S = 0.3445  # underlying/spot/stock price
K = 0.1284  # strike
r = -0.0045  # risk-free rate
t = 0.6504  # time to expiration in years => days to expiry / 365
C0 = 0.2163  # market price

#  Starting guess for the implied volatility.  Choose 0.5 arbitrarily.
vol = 0.5

epsilon = 1.0  # Define variable to check stopping conditions
abstol = 1e-8  # Stop calculation when abs(epsilon) < this number

i = 0  # Variable to count number of iterations
max_iter = 1e3  # Max number of iterations before aborting

while epsilon > abstol:
    #  if-statement to avoid getting stuck in an infinite loop.
    if i > max_iter:
        print('Program failed to find a root.  Exiting.')
        break

    i += 1
    orig = vol
    d1, d2 = d(vol, S, K, r, t)
    function_value = call_price(vol, S, K, r, t, d1, d2) - C0
    # print('call price:', call_price(vol, S, K, r, t, d1, d2))
    vega = S * norm.pdf(d1) * sqrt(t)
    vol = -function_value/vega + vol
    epsilon = abs(function_value)

print('Implied volatility = ',  vol)
print('Code required', i, 'iterations.')


vol = 0.1

epsilon = 1.0  # Define variable to check stopping conditions
abstol = 1e-8  # Stop calculation when abs(epsilon) < this number

i = 0  # Variable to count number of iterations
max_iter = 1e3  # Max number of iterations before aborting

while epsilon > abstol:
    #  if-statement to avoid getting stuck in an infinite loop.
    if i > max_iter:
        print('Program failed to find a root.  Exiting.')
        break

    i += 1
    orig = vol
    d1, d2 = d(vol, S, K, r, t)
    function_value = put_price(vol, S, K, r, t, d1, d2) - C0
    print('put price:', put_price(vol, S, K, r, t, d1, d2))
    vega = S * norm.pdf(d1) * sqrt(t)
    vol -= function_value/vega
    epsilon = abs(function_value)

print('Implied volatility = ',  vol)
print('Code required', i, 'iterations.')
