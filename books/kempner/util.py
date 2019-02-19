from functools import partial
import pandas as pd
import numpy as np
import sage.all as sg


from .sets import create_B, create_f, create_A, create_S
from .psi import a_coeff, psi

assert 0 ** 0 == 1


def create_matrices(matrix, digits):
    S = create_S(matrix.values, digits)
    f = create_f(matrix.values)
    A = create_A(matrices=[f[:,:,s] for s in range(f.shape[-1])])
    return S, f, A, create_B(A)


def Psi_matrix(matrix, digits, cutoff=30, extrapolation = 100, prec=None):
    #assert isinstance(S, pd.DataFrame)
    S = create_S(matrix.values, digits)


    #digits = S.shape[0]

    Psi = {k: S.applymap(partial(psi, k=k, prec=prec)) for k in range(1, cutoff)}

    for k in Psi.keys():
        Psi[k] = Psi[k].append(pd.DataFrame(columns=Psi[k].columns, data=sg.Rational(0),
                                            index=list(range(digits + 1, extrapolation))))

    for i in range(digits + 1, extrapolation):
        for k in Psi.keys():
            for index, www in np.ndenumerate(matrix):
                if www > 0:
                    for w in range(extrapolation - k):
                        if Psi[k+w][int(index[0]+1)][int(i-1)] > 1e-200:
                            a = a_coeff(k, w, index[1], prec=500, base=matrix.shape[1])
                            Psi[k][www][i] += a * Psi[k+w][int(index[0]+1)][int(i-1)]

    return Psi


def forward_interpolate(Psi, matrix):
    for k in range(Psi.shape[1]):
        if Psi[1,k,0] == 0:
            aaa = k
            break

    # forward interpolate rows of Psi
    for i in range(aaa, Psi.shape[1]):
        for k in range(1, Psi.shape[0]):
            for index, www in np.ndenumerate(matrix):
                if www > 0:
                    for w in range(Psi.shape[2] - k):
                        if Psi[k+w, i - 1, index[0]] > 1e-200:
                            a = a_coeff(k, w, index[1], prec=500, base=matrix.shape[1])
                            Psi[k, i, www-1] += a * Psi[k+w, i - 1, index[0]]

    return Psi


def forward_interpolate2(Psi, matrix, digits, extrapolation=30):
    aaa = digits + 1
    # append zero rows for forward interpolation
    #for k in Psi.keys():
    #    Psi[k] = Psi[k].append(pd.DataFrame(columns=Psi[k].columns, data=sg.Rational(0),
    #                                        index=list(range(aaa, extrapolation))))

    # find first row
    #B = Psi[1]
    #for k in B.index:
    #    if B[int(1)][k] == 0:
    #        aaa = k
    #        break

    # important start with i digit numbers...

    for i in range(aaa, extrapolation):
        for k in Psi.keys():
            for index, www in np.ndenumerate(matrix):
                if www > 0:
                    for w in range(extrapolation - k):
                        if Psi[k+w][int(index[0]+1)][int(i-1)] > 1e-200:
                            a = a_coeff(k, w, index[1], prec=500, base=matrix.shape[1])
                            Psi[k][www][i] += a * Psi[k+w][int(index[0]+1)][int(i-1)]

    return Psi
