import csv
from src import all_dirty_cells, csvToMatrix
from src import missing_data, isIncorrectDataType, is_outlier, is_na
import numpy as np

def test_dirty_cells():
    mat = csvToMatrix('tests/test_sheet_1.csv')
    inds, reasons = all_dirty_cells(mat, header = 1)
    assert inds.shape == (7, 2)
    assert reasons.shape == (7,)
    assert np.all(inds[0] == [0, 1])
    assert reasons[0] == missing_data
    assert np.all(inds[1] == [1, 6])
    assert reasons[1] == isIncorrectDataType
    assert np.all(inds[2] == [3, 4])
    assert reasons[2] == isIncorrectDataType
    assert np.all(inds[3] == [3, 6])
    assert reasons[3] == is_na
    assert np.all(inds[4] == [4, 3])
    assert reasons[4] == missing_data
    assert np.all(inds[5] == [5, 3])
    assert reasons[5] == missing_data
    assert np.all(inds[6] == [5, 6])
    assert reasons[6] == is_outlier
    