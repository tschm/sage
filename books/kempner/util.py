import numpy as np
import sage.all as sg

assert 0**0 == 1


def __shift_append(set, digit):
    return {a * 10 + digit for a in set}

def create_matrices(matrix, digits):
    S = np.empty((digits, matrix.shape[0]), dtype=set)
    # each element is explicitly set to be a set
    for index, x in np.ndenumerate(S):
        S[index] = set()

    # iterate over part of the first row
    for i, w in enumerate(matrix[0, 1:], 1):
        if w > 0:
            S[0, w - 1].add(i)

    # start with 2 digit numbers
    for d in range(1, digits):
        # loop over each T
        for index, w in np.ndenumerate(matrix):
            if w > 0:
                # append the scalar j to the d-1 digit numbers in S[i]
                S[d][w - 1] = S[d][w - 1].union(__shift_append(S[d - 1][index[0]], index[1]))

    # each element of the matrix S is not a sage vector
    for index, x in np.ndenumerate(S):
        S[index] = sg.vector(sg.ZZ, sorted(x))

    # create the matrices f
    #f = {j : np.zeros((matrix.shape[0], matrix.shape[0])) for j in range(matrix.shape[1])}

    f = np.zeros((matrix.shape[0], matrix.shape[0], matrix.shape[1]))

    # f[j,l,m] == 1 <=> T[l,m] = j is a matrix indicating whether
    # Append m to set l and end up in set j
    # For example "42"
    # S_1 set ending not in 4
    # S_2 set ending in 4
    # f[2] what if we append a 2?!
    # f[2][ ,1] we can append a 2 and end up in S_1 hence f[2][1,1] = 1  f[2][2,1] = 0
    # f[2][ ,2] we can't append a 2 to set in ending in 4, hence f[2][1,2] = 0

    i, j = np.where(matrix)
    for ii, jj in zip(i, j):
        f[matrix[ii, jj] - 1, ii, jj] = 1

    #print(sparse.csr_matrix(f))

    A = sg.matrix(sg.QQ, np.zeros((matrix.shape[0], matrix.shape[0])))

    #for s in f.values():
    #    A = A + sg.matrix(sg.QQ, s/10.0)
    for s in range(f.shape[-1]):
        A = A + sg.matrix(sg.QQ, f[:,:,s]/10.0)

    x = sg.matrix(sg.QQ, sg.matrix(sg.QQ, np.eye(matrix.shape[0]))-A)
    B = x.inverse() - sg.matrix(sg.QQ, np.eye(matrix.shape[0]))

    return S, f, A, B

# This is sage code
def __psi(x,k,prec=None):
    x_power = x.apply_map(lambda y: y**k)
    return sg.sum(x_power.apply_map(lambda y: sg.numerical_approx(1/y, digits=prec)))


def aCoeff( k,w,m, prec=None):
    if m+w==0:
        mw = sg.Rational(1)
    else:
        mw = __power(m, w)

    y = __power(0.1, k+w)*mw*__power(-1, w)*sg.binomial(k+w-1,w)

    if prec:
        y = sg.numerical_approx(y, digits=prec)

    return y

def __power(a,b):
    return sg.Rational(a)**b


def Psi_matrix(S, extrapolation=20, cutoff=30, prec=None):

    Psi = np.empty((extrapolation, S.shape[1], cutoff), dtype=object)

    for index, x in np.ndenumerate(Psi):
        Psi[index] = sg.Rational(0)

    # compute the sums Psi_{i} explicitly for up to 5 digits
    for index, s in np.ndenumerate(S):
        for k in range(1, cutoff):
            y = __psi(s, k, prec=prec)
            if y < 1e-100:
                break

            Psi[index[0], index[1], k] = y

    return Psi

def T_matrix(s):
    n = len(s)
    A = np.ones((n, 10), dtype=int)
    A[:, int(s[0])] = 2
    for n in range(1, len(s)):
        A[n, int(s[n])] = n + 2
    A[-1, int(s[-1])] = 0
    return A

def forward_interpolate(Psi, S, f):
    # forward interpolate rows of Psi
    for i in range(S.shape[0], Psi.shape[0]):
        for k in range(1, Psi.shape[2]):
            for index, x in np.ndenumerate(f):
                if x > 0:
                    for w in range(Psi.shape[2] - k):
                        if Psi[i - 1, index[1], k + w] > 1e-200:
                            Psi[i, index[0], k] = Psi[i, index[0], k] + aCoeff(k, w, index[2], prec=500) * Psi[
                                i - 1, index[1], k + w]

    return Psi

