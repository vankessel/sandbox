import numpy as np
import math as N


def soft_exponential(a, x):
    c = np.full_like(x, a)
    conditions = [
        c < 0,
        c == 0,
        c > 0
    ]
    functions = [
        lambda w: -np.log(1-a*(w+a))/a,
        lambda w: w,
        lambda w: (np.exp(a*w)-1)/a + a
    ]
    return np.piecewise(x, conditions, functions)


# Zeta func from https://codegolf.stackexchange.com/a/76246
def zeta_func(z, e=1e-9):
    r = z.real
    i = z.imag
    R = I = n = 0
    a = b = 1
    while a * a + b * b > e:
        a = b = 0
        p = 1
        m = 2 ** (-n-1)
        for k in range(1, n + 2):
            M = p / k ** r
            p *= (k - 1 - n) / k
            t = -i * N.log(k)
            a += M * N.cos(t)
            b += M * N.sin(t)
        a *= m
        b *= m
        R += a
        I += b
        n += 1
    A = 2 ** (1-r)
    t = -i * N.log(2)
    x = 1 - A * N.cos(t)
    y = A * N.sin(t)
    d = x * x + y * y
    if d != 0:
        return ((R * x - I * y) / d) + ((R * y + I * x) / d) * 1j
    else:
        return complex("nan")+complex("nanj")


zeta = np.vectorize(zeta_func)
