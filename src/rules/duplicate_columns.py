import pandas as pd
import numpy as np

def duplicate_columns(data):
    """Takes a whole dataset, returns which columns if any are redundant.
    Args:
        data (pd) : a panda dataframe

    Returns:
        duplicate_column_names (list) : list with names of redundant columns
    """
    duplicate_column_names = set()

    for x in range(data.shape[1]):
        col = data.iloc[:, x]
        for y in range(x + 1, data.shape[1]):
            otherCol = data.iloc[:, y]
            # Check if two columns at x & y index are equal or not
            if col.equals(otherCol):
                duplicate_column_names.add(data.columns.values[y])
    return list(duplicate_column_names)

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

