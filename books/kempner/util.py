import numpy as np
import sage.all as sg

assert 0 ** 0 == 1


def __shift_append(numbers, digit, base=10):
    return {a * base + digit for a in numbers}


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
                S[d][w - 1] = S[d][w - 1].union(__shift_append(S[d - 1][index[0]], index[1], base=matrix.shape[1]))

    # each element of the matrix S is not a sage vector
    for index, x in np.ndenumerate(S):
        S[index] = sg.vector(sg.ZZ, sorted(x))

    f = np.zeros((matrix.shape[0], matrix.shape[0], matrix.shape[1]))

    # f[j,l,m] == 1 <=> T[l,m] = j is a matrix indicating whether
    # Append m to set l and end up in set j

    i, j = np.where(matrix)
    for ii, jj in zip(i, j):
        f[matrix[ii, jj] - 1, ii, jj] = 1

    A = sg.matrix(sg.QQ, np.zeros((matrix.shape[0], matrix.shape[0])))

    for s in range(f.shape[-1]):
        A = A + sg.matrix(sg.QQ, f[:, :, s] / 10.0)

    x = sg.matrix(sg.QQ, sg.matrix(sg.QQ, np.eye(matrix.shape[0])) - A)
    B = x.inverse() - sg.matrix(sg.QQ, np.eye(matrix.shape[0]))

    return S, f, A, B


def __psi(x, k, prec=None):
    x_power = x.apply_map(lambda y: y ** k)
    return sg.sum(x_power.apply_map(lambda y: sg.numerical_approx(1 / y, digits=prec)))


def __a_coeff(k, w, m, prec=None, base=10):
    if m + w == 0:
        mw = sg.Rational(1)
    else:
        mw = __power(m, w)

    y = __power(1.0/base, k + w) * mw * __power(-1, w) * sg.binomial(k + w - 1, w)

    if prec:
        y = sg.numerical_approx(y, digits=prec)

    return y


def __power(a, b):
    return sg.Rational(a) ** b


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


def T_matrix(strings, base=10):
    if isinstance(strings, str):
        strings = [strings]

    feasible = sorted(list(split_strings(strings)), key=len)

    A = np.ones((len(feasible), base), dtype=int)
    B = np.empty((len(feasible), base), dtype=object)

    for index, b in np.ndenumerate(A):
        B[index] = "{base}{digit}".format(digit=str(index[1]), base=feasible[index[0]])

    for n, f in enumerate(feasible):
        for index, _ in np.ndenumerate(A):
            if B[index].endswith(f):
                A[index] = n + 1

    for string in strings:
        for index, _ in np.ndenumerate(A):
            if B[index].endswith(string):
                A[index] = 0

    return A


def split_string(string):
    return set([string[:w] for w in range(len(string))])


def split_strings(strings):
    if isinstance(strings, str):
        strings = [strings]

    # define an empty set
    ends = set([])

    for string in strings:
        words = split_string(string)

        already = False
        for word in words:
            if word in strings:
                # there is no need to include this string as already matched...
                already = True

        # print("union")
        if not already:
            ends = ends.union(words)

    return ends


def forward_interpolate(Psi, f):
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
                        if Psi[i - 1, index[1], k + w] > 1e-200:
                            Psi[i, index[0], k] = Psi[i, index[0], k] + __a_coeff(k, w, index[2], prec=500, base=f.shape[2]) * Psi[
                                i - 1, index[1], k + w]

    return Psi
