import numpy as np
import sage.all as sg

assert 0**0 == 1

def shift_append(set, digit):
    return {a * 10 + digit for a in set}

def create_S2(matrix, digits=5):
    S = np.empty((matrix.shape[0], digits), dtype=set)

    # each element is explicitly set to be a set
    for i in range(0, matrix.shape[0]):
        for j in range(0, digits):
            S[i,j] = set()

    # iterate over first row of the matrix
    for i in range(1, 10):
        S[matrix[0, i]-1,0].add(i)

    # start with 2 digit numbers
    for d in range(1, digits):
        # loop over each T
        for i, row in enumerate(matrix):
            for j, w in enumerate(row):
                if w > 0:
                    # append the scalar j to the d-1 digit numbers in S[i]
                    S[w-1][d] = S[w-1][d].union(shift_append(S[i][d - 1], j))


    for i in range(0, matrix.shape[0]):
        for j in range(0, digits):
            S[i,j] = sg.vector(sg.ZZ, S[i,j])

    return S

# This is sage code
def __psi(x,k,prec):
    return sg.numerical_approx(sg.sum(x.apply_map(lambda y: 1/y**k)), digits=prec)

psi = np.vectorize(__psi, excluded={"k", "digits"})

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

    return 10^(-k-w)*mw*(-1)^w*sg.binomial(k+w-1,w)

