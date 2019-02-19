import pytest
import numpy as np
import numpy.testing as npt
import sage.all as sg
from kempner.sets import create_B, create_S

from kempner.strings import T_matrix


@pytest.fixture
def matrix_42():
    return T_matrix("42", base=10)


@pytest.fixture()
def matrix_empty():
    return T_matrix(["0","1"], base=2)

def test_create_B(matrix_42):
    B = create_B(matrix_42)
    print(B)
    npt.assert_array_equal(B, np.array([[89, 80],[10,9]]))


def test_create_B_empty(matrix_empty):
    B = create_B(matrix_empty)
    assert B.size == 0


def test_create_S(matrix_42):
    s = create_S(matrix_42.values, digits=3)
    print(s)
    assert s[2][1] == sg.vector(sg.ZZ, [4])
    assert s[1][1] == sg.vector(sg.ZZ, [1,2,3,5,6,7,8,9])
    assert s[2][2] == sg.vector(sg.ZZ, [14,24,34,44,54,64,74,84,94])
    for x in s[1][2]:
        assert not x == 42
        assert not str(x).endswith("4")

    assert len(s[1][2]) == 80

    #assert False
