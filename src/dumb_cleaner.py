import numpy as np
from .rules import missing_data, is_na, isIncorrectDataType, is_outlier, wrong_cat, has_typo
from .rules import clean_missing, clean_na, clean_outlier, clean_wrong_cat, clean_wrong_dtype, clean_typo

def clean_cell_dumb(cell_str, col, reason):
    """Uses a dumber but simpler model for imputing cell type.
    
    Args:
        cell_str (str) : the cell to clean
        col (Column) : a container class with information about the cell's column
        reason (function) : a predicate representing why the cell is dirty

    Returns:
        predicted (str) : what the model predicts should go in that cell
    """
    if reason == has_typo:
        return clean_typo(cell_str)
    funcs = {missing_data : clean_missing,
             is_na : clean_na,
             isIncorrectDataType : clean_wrong_dtype,
             is_outlier : clean_outlier,
             wrong_cat : clean_wrong_cat}
    return funcs[reason](col)
