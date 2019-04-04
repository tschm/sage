import sage.all as sg

assert 0 ** 0 == 1
from backports.functools_lru_cache import lru_cache

def psi(x, k, prec):
    if len(x) == 0 or (x[0] ** k) > 10**prec:
        return sg.Rational(0.0)

    x_power = x.apply_map(lambda y: y ** k)
    return sg.sum(x_power.apply_map(lambda y: sg.numerical_approx(1 / y, digits=prec)))


def a_coeff(k, w, m, prec=None, base=10):
    #print(k,w,m)
    if m + w == 0:
        mw = sg.Rational(1)
    else:
        mw = __power(m, w)

    y = __power(1.0/base, k + w) * mw * __power(-1, w) * __binomial(k + w - 1, w)

    if prec:
        y = sg.numerical_approx(y, digits=prec)

    return y

@lru_cache()
def __binomial(a, b):
    return sg.binomial(a, b)

@lru_cache()
def __power(a, b):
    return sg.Rational(a) ** b


