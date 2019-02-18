import pandas as pd
import pandas.util.testing as pdt
from kempner.strings import T_matrix


def test_erdoes_borwein():
    A = T_matrix(strings=["0"], base=2)
    pdt.assert_frame_equal(A, pd.DataFrame(index=[""], columns=[0, 1], data=[[0,1]]))

def test_even_numbers():
    A = T_matrix(strings=["0","2","4","6","8"], base=10)
    pdt.assert_frame_equal(A, pd.DataFrame(index=[""], columns=range(0, 10), data=[[0,1,0,1,0,1,0,1,0,1]]))

def test_sub_numbers():
    A = T_matrix(strings=["3", "335"], base=6)
    pdt.assert_frame_equal(A, pd.DataFrame(index=[""], columns=range(0, 6), data=[[1,1,1,0,1,1]]))

def test_multiple_digits():
    A = T_matrix(strings=["42"], base=5)
    pdt.assert_frame_equal(A, pd.DataFrame(index=["","4"], columns=range(0,5), data=[[1,1,1,1,2],[1,1,0,1,2]]))

def test_multiple_strings():
    A = T_matrix(strings=["44","54"], base=6)
    pdt.assert_frame_equal(A, pd.DataFrame(index=["","5","4"], columns=range(0,6), data=[[1, 1, 1, 1, 3, 2],[1,1,1,1,0,2],[1,1,1,1,0,2]]))
