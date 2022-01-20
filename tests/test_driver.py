import csv
from src import all_dirty_cells, csvToMatrix
from src import missing_data, isIncorrectDataType, is_outlier, is_na
import numpy as np

def test_dirty_cells():
    mat = csvToMatrix('tests/test_sheet_1.csv')
    has_zero = False
    for row in mat:
        for col in row:
            if col == '':
                has_zero = True
                break
        else:
            continue
        break
    assert has_zero

    inds, reasons = all_dirty_cells(mat, header = 1)
    right_inds = np.array([[0, 1],
                           [0, 2],
                           [0, 7],
                           [1, 6],
                           [4, 3],
                           [5, 3],
                           [5, 6]])
    right_reasons = [missing_data, 
                     is_outlier,
                     is_outlier,
                     isIncorrectDataType,
                     is_na,
                     missing_data,
                     is_outlier]
    assert np.all(inds == right_inds)
    assert np.all(reasons == right_reasons)

    seq_inds, seq_reasons = all_dirty_cells(mat, header = 1, parallel = False)
    assert np.all(inds == seq_inds)
    assert np.all(reasons == seq_reasons)
    