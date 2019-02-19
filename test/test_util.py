import pytest
from kempner.strings import T_matrix
from kempner.util import Psi_matrix, extrapolate
import sage.all as sg
from kempner.psi import psi

@pytest.fixture
def matrix_42():
    return T_matrix("42", base=10)

def test_psi_matrix(matrix_42):
    p = Psi_matrix(matrix_42, digits=3, prec=20, extrapolation=50, cutoff=30)
    print(p)
    mm = p[1]
    assert mm[0,1] == 0.25    # 1/4 ! there is only one element in the 1-digit set for S_2
    assert mm[0,0] == psi(x=sg.vector(sg.ZZ, [1,2,3,5,6,7,8,9]), k=1, prec=20)
    assert mm[1,1] == psi(x=sg.vector(sg.ZZ, [14,24,34,44,54,64,74,84,94]), k=1, prec=20)

    mm = p[2]
    assert mm[0,1] == 1.0/16    # 1/16 ! there is only one element in the 1-digit set for S_2
    assert mm[0,0] == psi(x=sg.vector(sg.ZZ, [1,2,3,5,6,7,8,9]), k=2, prec=20)
    assert mm[1,1] == psi(x=sg.vector(sg.ZZ, [14,24,34,44,54,64,74,84,94]), k=2, prec=20)
    # assert False

    assert len(p) == 30 - 1
    assert p[1].shape[0] == 50
    assert p[1].shape[1] == 2
    assert 0 not in p.keys()

    x = extrapolate(matrix_42, p, prec=20)
    assert x == pytest.approx(228.44630415923081326, 0.0001)

    #assert False

