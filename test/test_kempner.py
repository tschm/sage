# content of test_sample.py
from kempner.util import split_string, split_strings, T_matrix
import numpy.testing as npt
import numpy as np


def test_split_string():
    s = split_string("42")
    assert s == {'', '4'}


def test_split_strings():
    s = split_strings(["42", "43"])
    assert s == {'', '4'}

    s = split_strings(["4444", "44"])
    assert s == {'', '4'}

    s = split_strings(["44", "54"])
    assert s == {'', '4', '5'}


def test_T_matrix():
    A = T_matrix(strings=["0"], base=2)
    npt.assert_array_equal(A, np.array([[0,1]]))
