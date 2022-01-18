import numpy as np
import pandas as pd
from .num_outliers import is_outlier
from ._column_temp import Column
from .utilities import can_be_float

def all_dirty_cells(csv_mat):
    preds = [is_outlier]
    dirty = []
    columns = get_all_cols(csv_mat)

    for row in range(csv_mat.shape[0]):
        for col in range(csv_mat.shape[1]):
            for pred in preds:
                if pred(csv_mat[row, col], columns[col]):
                    dirty.append((row, col, pred))
                    break
    
    return dirty

def get_all_cols(csv_mat):
    # mean, stddev, column_type
    # column is either 'num' or 'alpha'
    cols = [ Column() for _ in range(csv_mat.shape[1]) ]
    al_num_counts = [ [0, 0] for _ in range(csv_mat.shape[1]) ]

    for row in range(csv_mat.shape[0]):
        for col in range(csv_mat.shape[1]):
            al_num_counts[int(can_be_float(csv_mat[row, col]))] += 1
    
    for col in range(len(cols)):
        pass