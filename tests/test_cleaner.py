from src import clean_cell, csvToMatrix, all_dirty_cells
from src import get_models, set_models, clean_cell_dumb
from src import is_na
import numpy as np

ENABLED = False

def test_cleaner():
    # TODO : how tf do we handle mixed string and numeric data?
    # all our data will be dirty. We need tolerant models
    if ENABLED:
        mat = csvToMatrix('tests/test_sheet_1.csv')[1:]
        inds, reasons, cols = all_dirty_cells(mat, return_cols = True)
        # for model_type in ['auto', 'knn', 'deep', 'deep learning', 'naive bayes']:
        for model_type in ['forest']:
            set_models(None, None)
            for pair in range(inds.shape[0]):
                sugg = clean_cell(mat, 
                                  inds[pair], 
                                  cols[inds[pair, 1]], 
                                  model_type = model_type)
                assert type(sugg) == str
                assert not reasons[pair](sugg, cols[inds[pair, 1]])
                col_models, fitted_models = get_models()
                assert fitted_models[inds[pair, 1]]
                assert col_models is not None

def test_dumb_cleaner():
    mat = csvToMatrix('tests/test_sheet_1.csv')[1:]
    inds, reasons, cols = all_dirty_cells(mat, return_cols = True)
    for pair in range(inds.shape[0]):
        sugg = clean_cell_dumb(cols[inds[pair, 1]], reasons[pair])
        assert type(sugg) == str
        assert not reasons[pair](sugg, cols[inds[pair, 1]])
