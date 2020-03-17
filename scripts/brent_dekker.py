

# the brent-dekker algorithm iteratively finds the root of a function (f) that lies between two starting points (a, b)
# the function will automaticaly break after 'max_iter' number of iterations (although this isn't expected to be necessary),
# or if a solution is found with a tolerance of 'tolerance'
def brent_dekker(f, a, b, max_iter=50, tolerance=1e-8, return_num_of_steps=False):

    # verifies that initial guesses lie either side of the root, else returns 'nan'
    if (f(a) * f(b)) > 0:
        if return_num_of_steps:
            return float('nan'), 0
        else:
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

    if return_num_of_steps:
        return b, steps_taken
    else:
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
    if ((s < ((3 * a + b) / 4) or s > b) or
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

    root, steps = brent_dekker(
        f, 3, 5, tolerance=10e-8, return_num_of_steps=True)
    print('root is: {}'.format(root))
    print('steps taken: {}'.format(steps))

    root, steps = brent_dekker(
        f, 2.5, 5.5, tolerance=10e-8, return_num_of_steps=True)
    print('root is: {}'.format(root))
    print('steps taken: {}'.format(steps))

    root, steps = brent_dekker(
        g, -4, 0.006, tolerance=10e-8, return_num_of_steps=True)
    print('root is: {}'.format(root))
    print('steps taken: {}'.format(steps))
