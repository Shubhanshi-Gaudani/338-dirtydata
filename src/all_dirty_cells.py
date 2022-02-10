import numpy as np
import pandas as pd
from .rules import is_outlier
from .column import Column
from .rules import is_na
from .rules import isIncorrectDataType
from .rules import missing_data
import multiprocessing as mp
from itertools import starmap
from .rules import str_outlier
from .rules import wrong_cat
from .rules import has_typo

_NPROCS = 8
# predicates are called in order so order matters
_ALL_PREDS = [missing_data, is_na, isIncorrectDataType, is_outlier, has_typo, wrong_cat]

def analyze_cols(csv_mat, parallel = True):
    """Analyzes each column into Column objects.
    
    Args:
        csv_mat (np.array) : a 2D array of strings to analyze
        parallel (bool) : whether to analyze in parallel. Default is True

    Returns:
        cols (list) : a list of Column objects
    """
    if parallel:
        with mp.Pool(min(_NPROCS, csv_mat.shape[1])) as pool:
            return pool.map(Column, csv_mat.T)
    return list(map(Column, csv_mat.T))

def all_dirty_cells(csv_mat, header = 0, parallel = True, preds = None, return_cols = False):
    """Uses each predicate rule to find all dirty cells.

    Args:
        csv_mat (np.array) : a 2D array of strings to look through
        header (int) : how many rows at the top to skip.
            Default is zero, meaning no rows are skipped
        parallel (bool) : whether or not to compile the dirty cells
            in parallel. Default is True.
        preds (list) : a list of functions to call on each cell
        return_cols (bool) : whether to return the analyzed columns. Default is False

    Returns:
        dirty (np.array) : a array of [y, x] pairs that can be used to index into 
            csv_mat
        reasons (np.array) : an array of functions that the cells in 
            dirty failed. reasons[i] is the reason why dirty[i] failed
        (if return_cols:) columns (list) : a list of Column objects
    """
    preds = _ALL_PREDS if preds is None else preds
    csv_mat = csv_mat[header:]
    columns = analyze_cols(csv_mat, parallel = parallel)

    args = [ (row, columns, preds) for row in csv_mat ]

    if parallel:
        with mp.Pool(min(_NPROCS, csv_mat.shape[0])) as pool:
            is_dirty = np.array(pool.starmap(_dirty_row, args), dtype = object)
    else:
        is_dirty = np.array(list(starmap(_dirty_row, args)), dtype = object)

    not_none = is_dirty != None
    tup = np.argwhere(not_none), is_dirty[not_none]
    if return_cols: tup += (columns,)
    return tup

def _dirty_row(row, cols, preds):
    """Worker function for all_dirty_cells"""
    new_row = [None] * len(row)
    for col in range(len(row)):
        for pred in preds:
            if pred(row[col], cols[col]):
                new_row[col] = pred
                break
    return new_row
