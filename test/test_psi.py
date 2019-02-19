import sage.all as sg
from kempner.psi import psi, a_coeff
import pytest


def test_create_psi():

    x = psi(x=sg.vector(sg.ZZ, [5,6,7]), k=10, prec=20)
    assert 1.2247830486256163744e-7 == pytest.approx(x, 1e-10)

    x = psi(x=sg.vector(sg.ZZ, [5,6,7]), k=300, prec=20)
    assert x == sg.Rational(0)

    x = psi(x = [], k=200, prec=20)
    assert x == sg.Rational(0)

def test_a_coeff():
    x = a_coeff(5, w=0, m=0, prec=200, base=10)
    #print(x)
    #assert False
    assert 0.00001 == pytest.approx(x, 1e-10)
    #a_coeff(k, w, m, prec=None, base=10)
    #

