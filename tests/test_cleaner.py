from src import clean_cell, csvToMatrix, all_dirty_cells, has_header, arr_to_set, clean_all_cells
import numpy as np

def test_dumb_cleaner():
    mat = csvToMatrix('tests/test_sheet_1.csv')
    assert has_header(mat) == 1
    inds, reasons, cols = all_dirty_cells(mat, return_cols = True, header = 1)
    s_inds = arr_to_set(inds)
    suggs = clean_all_cells(mat, inds, reasons, cols)
    real_inds = np.array([ [inds[i, 0] - 1, inds[i, 1]] for i in range(inds.shape[0]) ])
    for pair in range(inds.shape[0]):
        sugg = clean_cell(real_inds[pair],
                          mat[1:], 
                          cols[real_inds[pair, 1]], 
                          reasons[pair],
                          s_inds)
        assert type(sugg) == str
        assert not reasons[pair]().is_dirty(sugg, cols[inds[pair, 1]])
        assert sugg == suggs[pair]
    

