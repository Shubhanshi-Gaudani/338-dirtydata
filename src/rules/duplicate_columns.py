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

# code from https://www.geeksforgeeks.org/how-to-find-drop-duplicate-columns-in-a-pandas-dataframe/

def redundant_columns(data):
    """Takes a whole dataset, returns which columns if any are redundant.
        Args:
            data (pd) : a panda dataframe

        Returns:
            red_columns (list) : list with pairs of names of redundant columns
        """
    redundant_column_names = set()
    for column2 in data:
        for column1 in data:
            if column1 == column2:
                break
            a = data.groupby(column1)[column2].transform(len)
            b = data.groupby(column2)[column1].transform(len)
            if a.equals(b):
                redundant_column_names.add((column1, column2))
    print(list(redundant_column_names))

