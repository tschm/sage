import numpy as np
import sage.all as sg

assert 0**0 == 1


def __shift_append(set, digit):
    return {a * 10 + digit for a in set}


def create_S3(matrix, digits=3):
    S = np.empty((digits, matrix.shape[0]), dtype=set)
    # each element is explicitly set to be a set
    for index, x in np.ndenumerate(S):
        S[index] = set()

    # iterate over part of the first row
    for i, w in enumerate(matrix[0, 1:], 1):
        S[0, w-1].add(i)

    # start with 2 digit numbers
    for d in range(1, digits):
        # loop over each T
        for index, w in np.ndenumerate(matrix):
            if w > 0:
                # append the scalar j to the d-1 digit numbers in S[i]
                S[d][w-1] = S[d][w-1].union(__shift_append(S[d - 1][index[0]], index[1]))

    for index, x in np.ndenumerate(S):
        S[index] = sg.vector(sg.ZZ, sorted(x))

    return S


# This is sage code
def psi(x,k,prec=None):
    y = sg.sum(x.apply_map(lambda y: 1/y**k))
    if prec:
        return sg.numerical_approx(y, digits=prec)
    else:
        print(type(y))
        return y


psi2 = np.vectorize(psi, excluded={"k", "prec"})


def create_f(matrix):
    i, j = np.where(matrix)
    f = np.zeros((matrix.shape[0], matrix.shape[0], matrix.shape[1]))

    for ii, jj in zip(i, j):
        f[matrix[ii, jj] - 1, ii, jj] = 1

    A = sg.matrix(sg.QQ, np.zeros((matrix.shape[0], matrix.shape[0])))

    for s in range(0, matrix.shape[1]):
        A = A + sg.matrix(sg.QQ, f[:,:,s]/10.0)

    x = sg.matrix(sg.QQ, sg.matrix(sg.QQ, np.eye(matrix.shape[0]))-A)
    B = x.inverse() - sg.matrix(sg.QQ, np.eye(matrix.shape[0]))

    return f, A, B


def aCoeff( k,w,m ):
    if m+w==0:
        mw = 1
    else:
        mw = m**w

    return sg.RealNumber(10^(-k-w)*mw*(-1)^w*sg.binomial(k+w-1,w))


def matrix_42():
    return np.array([[1, 1, 1, 1, 2, 1, 1, 1, 1, 1], [1, 1, 0, 1, 2, 1, 1, 1, 1, 1]])


def Psi_matrix(S, extrapolation=20, cutoff=30):

    Psi = np.empty((extrapolation, S.shape[1], cutoff), dtype=object)

    for index, x in np.ndenumerate(Psi):
        Psi[index] = sg.RealNumber("0.0")

    # compute the sums Psi_{i} explicitly for up to 5 digits
    for k in range(1, cutoff):
        for index, s in np.ndenumerate(S):
            y = psi(s, k, prec=100)
            Psi[index[0], index[1], k] = y

    return Psi
