import pandas as pd
import numpy as np

_QUANT_SCALE = 2

def _num_is_outlier(x, perc25, perc75, quant_scale = _QUANT_SCALE):
    """Takes a number and returns if it's an outlier."""
    iqr = perc75 - perc25
    return (x < perc25 - quant_scale * iqr or
            x > perc75 + quant_scale * iqr)

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

def outlier_message(cell_str, col):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the column

    Returns:
        message (str) : a readable reason why the string was dirty
    """
    med = col.quantile(0.5)
    above = 'above' if float(cell_str) > med else 'below'
    return f'This cell was way {above} the median, which was {med}.'
    