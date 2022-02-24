import numpy as np
from .rules import HasTypo
from .csv_to_matrix import has_header

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
    skip = has_header(sheet)
    sheet1 = sheet[skip:]
    real_inds = np.array([inds[0] - 1, inds[1]])
    return reason().clean(real_inds, sheet1, col)

