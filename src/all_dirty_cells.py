import numpy as np
import pandas as pd
from .num_outliers import is_outlier
from .column import Column
from .handle_na import is_na
from .is_correct_datatype import isIncorrectDataType
from .missing_data import missing_data
import multiprocessing as mp
from itertools import starmap
from .str_outlier import str_outlier

_NPROCS = 8
# predicates are called in order so order matters
_ALL_PREDS = [missing_data, is_na, isIncorrectDataType, is_outlier, str_outlier]

def all_dirty_cells(csv_mat, header = 0, parallel = True, preds = None):
    """Uses each predicate rule to find all dirty cells.

    Args:
        csv_mat (np.array) : a 2D array of strings to look through
        header (int) : how many rows at the top to skip.
            Default is zero, meaning no rows are skipped
        parallel (bool) : whether or not to compile the dirty cells
            in parallel. Default is True.

    Returns:
        dirty (np.array) : a array of [y, x] pairs that can be used to index into 
            csv_mat
        reasons (np.array) : an array of functions that the cells in 
            dirty failed. reasons[i] is the reason why dirty[i] failed
    """
    preds = _ALL_PREDS if preds is None else preds
    csv_mat = csv_mat[header:]
    columns = list(map(Column, csv_mat.T))

    nprocs = min(_NPROCS, csv_mat.shape[0])
    args = [ (row, columns, preds) for row in csv_mat ]

    if parallel:
        with mp.Pool(nprocs) as pool:
            is_dirty = np.array(pool.starmap(_dirty_row, args), dtype = object)
    else:
        is_dirty = np.array(list(starmap(_dirty_row, args)), dtype = object)

    not_none = is_dirty != None
    return np.argwhere(not_none), is_dirty[not_none]

def _dirty_row(row, cols, preds):
    """Worker function for all_dirty_cells"""
    new_row = [None] * len(row)
    for col in range(len(row)):
        for pred in preds:
            if pred(row[col], cols[col]):
                new_row[col] = pred
                break
    return new_row
