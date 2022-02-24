from src import clean_cell, csvToMatrix, all_dirty_cells, has_header
import numpy as np

def test_dumb_cleaner():
    mat = csvToMatrix('tests/test_sheet_1.csv')
    assert has_header(mat) == 1
    mat = mat[1:]
    inds, reasons, cols = all_dirty_cells(mat, return_cols = True)
    s_inds = set(map(tuple, inds))
    for pair in range(inds.shape[0]):
        sugg = clean_cell(inds[pair],
                          mat, 
                          cols[inds[pair, 1]], 
                          reasons[pair],
                          s_inds)
        assert type(sugg) == str
        assert not reasons[pair]().is_dirty(sugg, cols[inds[pair, 1]])
