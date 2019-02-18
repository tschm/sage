import numpy as np
import numpy.testing as npt
import sage.all as sg
from kempner.sets import create_A, create_B, create_f



def test_create_A():
    m1 = np.array([[1,0],[1,1]])
    m2 = np.array([[1,1],[1,1]])
    a = create_A([m1,m2])

    assert a[0,1] == sg.Rational(0.5)

    b = create_B(a)
    assert b[1,0] == sg.Rational(-2)

def test_create_f():
    m = np.array([[1,0],[1,2]])

    x = create_f(m)

    m1 = np.array([[1,0],[1,0]])
    m2 = np.array([[0,0],[0,1]])

    npt.assert_array_equal(x, np.array([m1, m2]))

