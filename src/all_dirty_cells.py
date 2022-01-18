import numpy as np
import pandas as pd
from .num_outliers import is_outlier
from .Column import Column

def all_dirty_cells(csv_mat):
    preds = [is_outlier]
    dirty = []
    columns = list(map(Column, csv_mat.T))

    for row in range(csv_mat.shape[0]):
        for col in range(csv_mat.shape[1]):
            for pred in preds:
                if pred(csv_mat[row, col], columns[col]):
                    dirty.append((row, col, pred))
                    break
    
    return dirty
