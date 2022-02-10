from ..utilities import can_be_float, can_be_int
from .missing_data import clean_missing
from .num_outliers import clean_outlier

def isIncorrectDataType(cell_str, col):
    """Returns whether cell_str's type does not match with col's type.

    Args:
        cell_str (str) : the raw text of that cell
        column (Column) : container for generic info about the column of that cell

    Returns:
        is_incorrect (bool) : whether that cell is the wrong type
    """
    if can_be_int(cell_str):
        return col.column_type != 'int' and col.column_type != 'float'
    if can_be_float(cell_str):
        return col.column_type != 'float'
    return col.column_type != 'alpha'    

def incorrect_dtype_message(cell_str, col):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the column

    Returns:
        message (str) : a readable reason why the string was dirty
    """
    interp_type = 'alphabetical'
    if can_be_int(cell_str):
        interp_type = 'an integer'
    elif can_be_float(cell_str):
        interp_type = 'a decimal number'
    true_type = 'alphabetical words'
    if col.column_type == 'int':
        true_type = 'integers'
    elif col.column_type == 'float':
        true_type = 'decimal numbers'
    return (f'The cell {cell_str} was interpreted as {interp_type}, in contrast ' +
            f"to the column's most common datatype, {true_type}.")

def clean_wrong_dtype(col):
    """Returns the desired imputed value based on data from col.
    
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
