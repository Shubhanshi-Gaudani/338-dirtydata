import numpy as np
import pandas as pd
from .num_outliers import is_outlier
from .Column import Column
import multiprocessing as mp

_NPROCS = 8
_ALL_PREDS = [is_outlier]

def all_dirty_cells(csv_mat):
    is_dirty = np.zeros(csv_mat.shape, dtype = bool)
    columns = list(map(Column, csv_mat.T))

    nprocs = min(_NPROCS, csv_mat.shape[0])
    args = [ (row, columns) for row in csv_mat ]

    with mp.Pool(nprocs):
        is_dirty = np.array(mp.starmap(_dirty_row, args), dtype = bool)
    return np.where(is_dirty)

def _dirty_row(row, cols):
    row = np.zeros(row.shape[0], dtype = bool)
    for col in range(row.shape[0]):
        for pred in _ALL_PREDS:
            if pred(row[col], cols[col]):
                row[col] = True
                break
    return row
