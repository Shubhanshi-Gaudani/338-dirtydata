import numpy as np
from .rules import missing_data, is_na, isIncorrectDataType, is_outlier

def clean_cell_dumb(col, reason):
    """Uses a dumber but simpler model for imputing cell type.
    
    Args:
        col (Column) : a container class with information about the cell's column
        reason (function) : a predicate representing why the cell is dirty

    Returns:
        predicted (str) : what the model predicts should go in that cell
    """
    funcs = {missing_data : clean_missing,
             is_na : clean_na,
             isIncorrectDataType : clean_wrong_dtype,
             is_outlier : clean_outlier}
    return funcs[reason](col)

def clean_na(col):
    """Returns the desired imputed vakue based on data from col.
    
    Args:
        col (Column) : a container class with information about the cell's column

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    return 'NA'

def clean_missing(col):
    """Returns the desired imputed vakue based on data from col.
    
    Args:
        col (Column) : a container class with information about the cell's column

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    return str(col.mode)

def clean_wrong_dtype(col):
    """Returns the desired imputed vakue based on data from col.
    
    Args:
        col (Column) : a container class with information about the cell's column

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    if col.column_type == 'alpha':
        return clean_missing(col)
    i = clean_outlier(col)
    if col.column_type == 'int':
        return str(int(float(i))) # this is so dumb
    return i

def clean_outlier(col):
    """Returns the desired imputed vakue based on data from col.
    
    Args:
        col (Column) : a container class with information about the cell's column

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    return str(col.quantile(0.5))
    