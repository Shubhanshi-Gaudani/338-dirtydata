import numpy as np
import pandas as pd
from .num_outliers import is_outlier
from .column import Column
from .handle_na import is_na
from .is_correct_datatype import isIncorrectDataType
from .missing_data import missing_data
import multiprocessing as mp

_NPROCS = 8
_ALL_PREDS = [missing_data, isIncorrectDataType, is_outlier, is_na]

def all_dirty_cells(csv_mat, header = 0):
    """Uses each predicate rule to find all dirty cells.

    Args:
        csv_mat (np.array) : a 2D array of strings to look through
        header (int) : how many rows at the top to skip.
            Default is zero, meaning no rows are skipped

    Returns:
        dirty (np.array) : a array of [y, x] pairs that can be used to index into 
            csv_mat
        reasons (np.array) : an array of functions that the cells in 
            dirty failed. reasons[i] is the reason why dirty[i] failed
    """
    columns = list(map(Column, csv_mat[header:].T))

    nprocs = min(_NPROCS, csv_mat.shape[0] - header)
    args = [ (row, columns) for row in csv_mat ]

    with mp.Pool(nprocs) as pool:
        is_dirty = np.array(pool.starmap(_dirty_row, args), dtype = object)
    not_none = is_dirty != None
    return np.argwhere(not_none), np.where(not_none, is_dirty)

def _dirty_row(row, cols):
    """Worker function for all_dirty_cells"""
    row = []
    for col in range(row.shape[0]):
        row.append(None)
        for pred in _ALL_PREDS:
            if pred(row[col], cols[col]):
                row[col] = pred
                break
    return row
