#Import necessary libraries 
import numpy as np 
import pandas as pd

def missing_data(cell_str, column):
    """Takes the string version of the cell and returns whether it is empty or not

    Args: 
        cell_str (str): the raw text of the cell
        column (column): contianer for generic in"fo about the container of that cell
    
    Returns: 
        output (bool) : returns True if empty, and False if not

    """
    if (cell_str.strip() == ""): 
        return True
    else:
        return False
    
def missing_message(cell_str, col):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the column

    Returns:
        message (str) : a readable reason why the string was dirty
    """
    return 'The cell is empty.'
