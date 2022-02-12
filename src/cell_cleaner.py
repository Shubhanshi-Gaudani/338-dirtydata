import numpy as np
from .rules import HasTypo

def clean_cell(inds, sheet, col, reason):
    """Uses a dumber but simpler model for imputing cell type.
    
    Args:
        inds (np.array) : a [y, x] pair indicating which cell to clean
        sheet (np.array) : a 2D matrix of strings
        col (Column) : a container class with information about the cell's column
        reason (function) : a predicate representing why the cell is dirty

    Returns:
        predicted (str) : what the model predicts should go in that cell
    """
    return reason().clean(inds, sheet, col)
