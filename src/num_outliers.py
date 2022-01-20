import pandas as pd
import numpy as np

_QUANT_SCALE = 2

def is_outlier(cell_str, col):
    """Takes the string version of the cell and returns whether it is an outlier.

    Also returns False if the cell cannot be cast as a float

    Args:
        cell_str (str) : the raw text of that cell
        col (Column) : container for generic info about the column of that cell

    Returns:
        is_outlier (bool) : whether that cell is an outlier numerically
    """
    try:
        f = float(cell_str)
    except ValueError:
        return False

    iqr = col.quants[3] - col.quants[1]
    return (f < col.quants[1] - _QUANT_SCALE * iqr or
            f > col.quants[3] + _QUANT_SCALE * iqr)
    