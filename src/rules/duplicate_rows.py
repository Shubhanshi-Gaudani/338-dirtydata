import pandas as pd
import numpy as np

def duplicate_row(data):
    """Takes a whole dataset, returns which rows if any are duplicates.

    Args:
        data (np.array) : a 2D array of strings

    Returns:
        dup_rows (list) : a list of row indices which are duplicates
    """
    rows = set()
    dupes = []
    for row in range(data.shape[0]):
        if data[row] in rows:
            dupes.append(row)
        else:
            rows.add(data[row])
    return dupes
