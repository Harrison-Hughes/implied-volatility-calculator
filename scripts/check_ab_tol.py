#!/usr/bin/env python3
from math import isclose


def check_for_absolute_tolerance(val_1, val_2, tol=10**-8):
    return isclose(val_1, val_2, rel_tol=tol)


print(f'{10**-8}')
print(check_for_absolute_tolerance(5, 5.1))  # false
print(check_for_absolute_tolerance(5, 5.00000001))  # true
