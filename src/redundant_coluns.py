import pandas as pd
import numpy as np

def duplicate_row(data):
    """Takes a whole dataset, returns which columns if any are redundant.

    Args:
        data (pd) : a panda dataframe

    Returns:
        dup_columns (list) : list with names of redundant columns
    """
    # Create an empty set
    duplicateColumnNames = set()

    # Iterate through all the columns
    # of dataframe
    for x in range(data.shape[1]):

        # Take column at xth index.
        col = data.iloc[:, x]

        # Iterate through all the columns in
        # DataFrame from (x + 1)th index to
        # last index
        for y in range(x + 1, data.shape[1]):

            # Take column at yth index.
            otherCol = data.iloc[:, y]

            # Check if two columns at x & y
            # index are equal or not,
            # if equal then adding
            # to the set
            if col.equals(otherCol):
                duplicateColumnNames.add(data.columns.values[y])

    # Return list of unique column names
    # whose contents are duplicates.
    return list(duplicateColumnNames)

# code from https://www.geeksforgeeks.org/how-to-find-drop-duplicate-columns-in-a-pandas-dataframe/