import numpy as np
from .rules import HasTypo

def clean_cell_dumb(cell_str, col, reason):
    """Uses a dumber but simpler model for imputing cell type.
    
    Args:
        cell_str (str) : the cell to clean
        col (Column) : a container class with information about the cell's column
        reason (function) : a predicate representing why the cell is dirty

    Returns:
        predicted (str) : what the model predicts should go in that cell
    """
    if reason == HasTypo:
        return HasTypo().clean(cell_str)
    return reason().clean(col)
