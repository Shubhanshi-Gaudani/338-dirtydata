def is_na(cell_str, column):
    """Takes the string version of the cell and returns whether it is a wrongly formatted NA.
    Args:
        cell_str (str) : the raw text of that cell
        column (Column) : container for generic info about the column of that cell
    Returns:
        is_na (bool) : whether that cell is a wrongly typed NA 
    """
    missing_values = {"n/a", "na", "--", "-","nan","NaN", "not applicable"}
    if cell_str.lower() in missing_values and cell_str != 'NA': 
        return True
    else:
        return False

def na_message(cell_str, col):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the column

    Returns:
        message (str) : a readable reason why the string was dirty
    """
    return (f'This cell "{cell_str}" was interpreted as a variation of "NA". ' +
            'We suggest standardizing all such cells to "NA".')

def clean_na(col):
    """Returns the desired imputed value based on data from col.
    
    Args:
        col (Column) : a container class with information about the cell's column

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    return 'NA'
