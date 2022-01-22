import pandas as pd
import numpy as np

_QUANT_SCALE = 2

def _num_is_outlier(x, perc25, perc75):
    """Takes a number and returns if it's an outlier."""
    iqr = perc75 - perc25
    return (x < perc25 - _QUANT_SCALE * iqr or
            x > perc75 + _QUANT_SCALE * iqr)

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
    
    return _num_is_outlier(f, col.quantile(0.25), col.quantile(0.75))