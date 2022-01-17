import pandas as pd
import numpy as np
from .utilities import can_be_float

_NUM_STDS = 4

def is_outlier(cell_str, column):
    """Takes the string version of the cell and returns whether it is an outlier.

    Also returns True if the cell cannot be cast as a float

    Args:
        cell_str (str) : the raw text of that cell
        column (Column) : container for generic info about the column of that cell

    Returns:
        is_outlier (bool) : whether that cell is an outlier numerically
    """
    if not can_be_float(cell_str): return True
    return abs(column.mean - float(cell_str)) > _NUM_STDS * column.stddev
    