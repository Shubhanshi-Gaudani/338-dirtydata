from ..utilities import can_be_float, can_be_int

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
        reason (function) : a function representing the reason why the cell
            was dirty.

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
