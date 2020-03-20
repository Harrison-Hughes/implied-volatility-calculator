from math import isnan

# the brent-dekker root finding algorithm iteratively finds the root of a function (f) that lies between two starting points (a, b)
# this version of the algorithm has been adapted to searching for implied volatility (to increase convergence speed) by having the bounds (bounds) as an array,
# such that the algorithm will iterate through the bounds if they do not lie either side of the solution (e.g. bounds =  [0, 1, 2, 5, 10, 100, 1000])

# the function will automaticaly break after 'max_iter' number of iterations (although this isn't expected to be necessary),
# or if a solution is found with a tolerance of 'tolerance'


def bd_var_bounds(f, bounds, max_iter=50, tolerance=1e-8):

    if f(bounds[0]) > 0:  # if even the lowest bound lies above the root, return nan
        return float('nan')

    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i+1]  # (a, b) are the pair of bounds
        if (f(a) * f(b)) <= 0:  # if (a, b) lie either side of the root, the algorithm continues
            break
        # if even the two largest bounds lie below the root, the algorithm returns nan
        if i == len(bounds) - 2:
            return float('nan')

    # if |f(a)| < |f(b)| then swap 'a' and 'b'
    # i.e. b should represent the 'best' guess
    if abs(f(a)) < abs(f(b)):
        a, b = b, a

    c = a  # throughout the algorithm, point 'c' will replace 'b' at the end of an iteration, however, it is initialised as equal to 'a'
    d = 0  # d is assigned here arbitrarily as it will not be used before the second iteration

    prev_iter_used_bi = True  # used to track whether the previous iteration used bisection
    steps_taken = 0

    # iterates until solution criteria are met
    while steps_taken < max_iter and abs(b - a) > tolerance and f(b) != 0.0 and f(c) != 0.0:
        a, b, c, d, prev_iter_used_bi = brent_dekker_iterative_converge(
            f, a, b, c, d, prev_iter_used_bi, tolerance)
        steps_taken += 1

    return b


def brent_dekker_iterative_converge(f, a, b, c, d, mflag, tolerance):
    f_a = f(a)
    f_b = f(b)
    f_c = f(c)

    # try to compute new point 's' with inverse quadratic interpolation (IQI)
    if f_a != f_c and f_b != f_c:
        s = inverse_quadratic_interpolation(a, b, c, f_a, f_b, f_c)

    # if cannot use IQI, the secant method is used to compute 's' intead
    else:
        s = secant_method(a, b, f_a, f_b)

    # the bisection method is called when certain criteria are met, and overrides the secant value for 's'
    if condition_for_bisection_method(a, b, c, d, s, mflag, tolerance):
        s = bisection_method(a, b)
        mflag = True

    else:
        mflag = False

    f_s = f(s)
    d, c = c, b  # update values

    if (f_a * f_s) < 0:  # ensures the root remains between 'a' and 'b'
        b = s
    else:
        a = s

    if abs(f_a) < abs(f_b):  # keep 'b' as the best guess
        a, b = b, a

    return a, b, c, d, mflag


def inverse_quadratic_interpolation(a, b, c, f_a, f_b, f_c):
    L0 = (a * f_b * f_c) / ((f_a - f_b) * (f_a - f_c))
    L1 = (b * f_a * f_c) / ((f_b - f_a) * (f_b - f_c))
    L2 = (c * f_b * f_a) / ((f_c - f_a) * (f_c - f_b))
    return L0 + L1 + L2


def secant_method(a, b, f_a, f_b):
    return b - ((f_b * (b - a)) / (f_b - f_a))


def condition_for_bisection_method(a, b, c, d, s, mflag, tolerance):
    # returns true if any of these occur:
    # i) s lies outside of the range of b and (3a + b) / 4
    # ii) previously used bisection and |s - b| >= |b - c| / 2
    # iii) did not previously use bisection and |s - b| >= |c - d| / 2
    # iv) previously used bisection and |b - c| < tolerance
    # v) did not previously use bisection and |c - d| < tolerance
    if ((not (3.0*a+b)/4.0 < s < b) or
        (mflag and (abs(s - b)) >= (abs(b - c) / 2)) or
        (not mflag and (abs(s - b)) >= (abs(c - d) / 2)) or
        (mflag and (abs(b - c)) < tolerance) or
            (not mflag and (abs(c - d)) < tolerance)):
        return True
    else:
        return False


def bisection_method(a, b):
    return (a + b) / 2.0


if __name__ == '__main__':
    def f(x): return x ** 2 - 20
    def g(x): return (x + 3) * (x - 1) ** 2

    root = bd_var_bounds(
        f, [3, 5], tolerance=10e-8)
    print('root is: {}'.format(root))

    root = bd_var_bounds(
        f, [2.5, 5.5], tolerance=10e-8)
    print('root is: {}'.format(root))

    root = bd_var_bounds(
        f, [4.4, 4.5], tolerance=10e-8)
    print('root is: {}'.format(root))

    root = bd_var_bounds(
        g, [-4, 0.006], tolerance=10e-8)
    print('root is: {}'.format(root))
