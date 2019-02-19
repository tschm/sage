import numpy as np
import pandas as pd

import sage.all as sg

assert 0 ** 0 == 1


def __shift_append(numbers, digit, base=10):
    return {a * base + digit for a in numbers}


def create_S(matrix, digits):
    assert isinstance(matrix, np.ndarray)

    S = pd.DataFrame(index=list(range(1, digits+1)), columns=list(range(1, matrix.shape[0] + 1)), dtype=object)

    for row in S.index:
        for col in S.columns:
            S[col][row] = set([])

    for x in range(1, matrix.shape[1]):
        # first row matrix...
        a = matrix[0, x]
        if a > 0:
            S[a][1].add(x)

    for d in range(2, digits+1):
        for index, w in np.ndenumerate(matrix):
            if w > 0:
                S[w][d] = S[w][d].union(__shift_append(S[index[0]+1][d-1], index[1], base=matrix.shape[1]))

    for row in S.index:
        for col in S.columns:
            S[col][row] = sg.vector(sg.ZZ, sorted(S[col][row]))

    return S


def __create_f(matrix):
    assert isinstance(matrix, np.ndarray)

    a = np.unique(matrix)
    # this looks very inefficient for a sparse matrix. We create a dense matrix of ones to multiply elementwise with the
    # sparse matrix == j
    f = {j: np.ones_like(matrix)*(matrix==j) for j in set(a[a > 0])}
    return np.array(f.values())


def create_B(matrix):
    f = __create_f(matrix.values)
    if f.size == 0:
        return np.array([[]])

    a = __create_A(matrices=[f[:, :, s] for s in range(f.shape[-1])])

    x = sg.matrix(sg.QQ, sg.matrix(sg.QQ, np.eye(a.nrows())) - a)
    b = x.inverse() - sg.matrix(sg.QQ, np.eye(a.nrows()))
    return b


def __create_A(matrices):
    return sg.Matrix(sg.QQ, sum(matrices)/(1.0*len(matrices)))