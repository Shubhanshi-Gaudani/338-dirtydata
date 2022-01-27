from .num_outliers import is_outlier, outlier_message
from .handle_na import is_na, na_message
from .is_correct_datatype import isIncorrectDataType, incorrect_dtype_message
from .missing_data import missing_data, missing_message

def user_message(cell_str, col, reason):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the cell's column
        reason (function) : a function representing the reason why the cell is dirty

    Returns:
        message (str) : a readable string for why the cell is dirty
    """
    funcs = {is_outlier : outlier_message,
             is_na : na_message,
             isIncorrectDataType : incorrect_dtype_message,
             missing_data : missing_message}
    return funcs[reason](cell_str, col)
    