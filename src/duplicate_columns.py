import pandas as pd
import numpy as np

def duplicate_columns(data):
    """Takes a whole dataset, returns which columns if any are redundant.
    Args:
        data (pd) : a panda dataframe

    Returns:
        dup_columns (list) : list with names of redundant columns
    """
    duplicateColumnNames = set()

    for x in range(data.shape[1]):
        col = data.iloc[:, x]
        for y in range(x + 1, data.shape[1]):
            otherCol = data.iloc[:, y]
            # Check if two columns at x & y index are equal or not
            if col.equals(otherCol):
                duplicateColumnNames.add(data.columns.values[y])
    return list(duplicateColumnNames)

# code from https://www.geeksforgeeks.org/how-to-find-drop-duplicate-columns-in-a-pandas-dataframe/