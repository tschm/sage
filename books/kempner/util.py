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


def Psi_matrix(S, extrapolation=20, cutoff=30, prec=None):
    Psi = np.empty((extrapolation, S.shape[1], cutoff), dtype=object)

    for index, x in np.ndenumerate(Psi):
        Psi[index] = sg.Rational(0)

    # compute the sums Psi_{i} explicitly for up to 5 digits
    for index, s in np.ndenumerate(S):
        for k in range(1, cutoff):
            Psi[index[0], index[1], k] = psi(s, k, prec=prec)

    return Psi

def Psi_matrix2(S, cutoff=30, prec=None):
    return {k : S.applymap(partial(psi, k=k, prec=prec)) for k in range(1, cutoff)}


def forward_interpolate(Psi, f, matrix):
    # todo: get rid of S here...
    for k in range(Psi.shape[0]):
        if Psi[k,0,1] == 0:
            aaa = k
            break

    # forward interpolate rows of Psi
    for i in range(aaa, Psi.shape[0]):
        for k in range(1, Psi.shape[2]):
            for index, x in np.ndenumerate(f):
                if x > 0:
                    for w in range(Psi.shape[2] - k):
                        c = Psi[i - 1, index[1], k + w]
                        if c > 1e-200:
                            a = a_coeff(k, w, index[2], prec=500, base=matrix.shape[1])
                            Psi[i, index[0], k] += a * c

    return Psi


def forward_interpolate2(Psi, f, extrapolation=30):
    # todo: get rid of S here...
    #print(Psi.keys())
    #print(Psi[1])
    #print(Psi[1].index)
    #A = pd.DataFrame(index=range(1, extrapolation), columns=Psi[1].columns)
    #A.loc[Psi[1].index] = Psi[1]

    for k in Psi.keys():
        A = pd.DataFrame(index=range(1, extrapolation), columns=Psi[k].columns, dtype=object)
        A.loc[Psi[k].index] = Psi[k]
        Psi[k] = A
        #print(Psi[k])

    #assert False

    # forward interpolate rows of Psi
    for k in Psi.keys():
        nmin = Psi[k].last_valid_index() + 1
        print(nmin)
        Psi[k] = Psi[k].fillna(sg.Rational(0))
        print(Psi[k].index[-1])
        print(Psi[k])

        # loop over all rows
        for i in range(nmin, Psi[k].index[-1]):
            print(i)
            for index, x in np.ndenumerate(f):
                if x > 0:
                    for w in range(len(Psi)-k):
                        print(Psi[k + w][index[1] + 1][i - 1])
                        a = a_coeff(k, w, index[2] + 1, prec=500, base=f.shape[2])
                        c = Psi[k+w][index[1]+1][i-1]
                        if c > 1e-200:
                            Psi[k][index[0]+1][i] += a * c

    return Psi
