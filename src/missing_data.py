#Import necessary libraries 
import numpy as np 
import pandas as pd

def missing_data(cell_str, column, replace_with):
    """Takes the string version of the cell and returns whether it is an outlier

    Args: 
        cell_str (str): the raw text of the cell
        column (column): contianer for generic in"fo about the container of that cell
        replace_with (string): "mean", "median", "mode", "remove"
    
    Returns: 
        output (str) : output value to replace the information with 

    """
    if (cell_str.strip() == ""): 
        if replace_with == 'mean':
            return str(column.mean)
        elif replace_with == 'median':
            return str(column.median)
        elif replace_with == 'mode':
            return str(column.mode)
        else: 
            return 'remove'
    

