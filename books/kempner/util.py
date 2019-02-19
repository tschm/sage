from functools import partial
import pandas as pd
import numpy as np
import sage.all as sg


from .sets import create_S, create_B
from .psi import a_coeff, psi

assert 0 ** 0 == 1


def Psi_matrix(matrix, digits, cutoff=30, extrapolation = 100, prec=None):
    # create explicitly the sets S for up to d digits.
    S = create_S(matrix.values, digits=digits)

    Psi = {k: S.applymap(partial(psi, k=k, prec=prec)) for k in range(1, cutoff)}

    # append zero rows...
    for k in Psi.keys():
        Psi[k] = Psi[k].append(pd.DataFrame(columns=Psi[k].columns, data=sg.Rational(0),
                                            index=list(range(digits, extrapolation)))).values

    limit = 10 ** (prec * (-1))

    for i in range(digits, extrapolation):
        for k in Psi.keys():
            if Psi[k][i - 1, 0] > 0:
                for index, www in np.ndenumerate(matrix):
                    if www > 0:
                        for w in range(extrapolation - k):
                            p = Psi[k+w][i-1,index[0]]
                            if p > limit:
                                a = a_coeff(k, w, index[1], prec=prec, base=matrix.shape[1])
                                Psi[k][i, www-1] += a * p
                            else:
                                break

    return Psi


def extrapolate(matrix, Psi, prec=None):
    v = Psi[1][-1, :]
    B = create_B(matrix)
    a = sum(sum(Psi[1]))
    b = sum(sum(B*v))
    if prec:
        return sg.numerical_approx(a + b, digits=prec)
    else:
        return a + b