from src import clean_cell, csvToMatrix, all_dirty_cells
import numpy as np

def test_dumb_cleaner():
    mat = csvToMatrix('tests/test_sheet_1.csv')[1:]
    inds, reasons, cols = all_dirty_cells(mat, return_cols = True)
    for pair in range(inds.shape[0]):
        sugg = clean_cell(inds[pair],
                          mat, 
                          cols[inds[pair, 1]], 
                          reasons[pair])
        assert type(sugg) == str
        assert not reasons[pair]().is_dirty(sugg, cols[inds[pair, 1]])
