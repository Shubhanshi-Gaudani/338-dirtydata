import pandas as pd
import numpy as np

def duplicate_columns(data):
    """Takes a whole dataset, returns which columns if any are redundant.
    Args:
        data (np.array) : a 2D array of strings

    Returns:
        duplicate_column_names (list) : list of column indices which are duplicates
    """
    cols = set()
    dupes = []
    posed = data.T
    tups = list(map(tuple, posed))
    for col in range(len(tups)):
        if tups[col] in cols:
            dupes.append(col)
        else:
            cols.add(tups[col])
    return dupes

def redundant_columns(data):
    """Takes a whole dataset, returns which columns if any are redundant.

    Args:
        data (np.array) : a 2D array of strings

    Returns:
        dupe_inds (list) : a list of (col_index1, col_index2) pairs, each of which
            is a tuple of redundant columns.
    """
    dupe_inds = []
    data = data.T
    for col1 in range(data.shape[0]):
        for col2 in range(data.shape[1]):
            mapping = {}
            for row in range(data.shape[1]):
                if (data[col1, row] in mapping and
                    mapping[data[col1, row]] != data[col2, row]):
                    break
                else:
                    mapping[data[col1, row]] = data[col2, row]

            else:
                dupe_inds.append((col1, col2))
    
    return dupe_inds

