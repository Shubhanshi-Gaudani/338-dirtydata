import pandas as pd
import numpy as np
from .utilities import can_be_float

_NUM_STDS = 4

def is_outlier(cell_str, col):
    """Takes the string version of the cell and returns whether it is an outlier.

    Also returns False if the cell cannot be cast as a float

    Args:
        cell_str (str) : the raw text of that cell
        col (Column) : container for generic info about the column of that cell

    Returns:
        is_outlier (bool) : whether that cell is an outlier numerically
    """
    if not can_be_float(cell_str): return False
    return abs(col.mean - float(cell_str)) > _NUM_STDS * col.stddev
    