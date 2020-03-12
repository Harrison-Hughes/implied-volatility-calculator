def brent_dekker(f, a, b, max_iter=50, tolerance=1e-8):

    f_a, f_b, d = f(a), f(b), 0

    assert (f_a * f_b) <= 0, "Root not bracketed"

    # if |f(x0)| < |f(x1)| then swap (a,b)
    if abs(f_a) < abs(f_b):
        a, b = b, a
        f_a, f_b = f_b, f_a

    x2, fx2 = a, f_a

    mflag = True
    steps_taken = 0

    while steps_taken < max_iter and abs(b-a) > tolerance:
        f_a = f(a)
        f_b = f(b)
        fx2 = f(x2)

        if f_a != fx2 and f_b != fx2:
            L0 = (a * f_b * fx2) / ((f_a - f_b) * (f_a - fx2))
            L1 = (b * f_a * fx2) / ((f_b - f_a) * (f_b - fx2))
            L2 = (x2 * f_b * f_a) / ((fx2 - f_a) * (fx2 - f_b))
            new = L0 + L1 + L2

        else:
            new = b - ((f_b * (b - a)) / (f_b - f_a))

        if ((new < ((3 * a + b) / 4) or new > b) or
            (mflag == True and (abs(new - b)) >= (abs(b - x2) / 2)) or
            (mflag == False and (abs(new - b)) >= (abs(x2 - d) / 2)) or
            (mflag == True and (abs(b - x2)) < tolerance) or
                (mflag == False and (abs(x2 - d)) < tolerance)):
            new = (a + b) / 2
            mflag = True

        else:
            mflag = False

        fnew = f(new)
        d, x2 = x2, b

        if (f_a * fnew) < 0:
            b = new
        else:
            a = new

        if abs(f_a) < abs(f_b):
            a, b = b, a

        steps_taken += 1

    return b, steps_taken


def f(x): return x**2 - 20


def g(x): return (x + 3) * (x - 1) ** 2


root, steps = brent_dekker(f, 3, 5, tolerance=10e-8)
print("root is:", root)
print("steps taken:", steps)

root, steps = brent_dekker(g, -4, 4/3.0, tolerance=10e-8)
print("root is:", root)
print("steps taken:", steps)
