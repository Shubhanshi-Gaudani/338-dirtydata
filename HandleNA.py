import pandas as pd
import numpy as np

def is_na(cell_str, column):
    """Takes the string version of the cell and returns whether it is a wrongly formatted NA.
    Args:
        cell_str (str) : the raw text of that cell
        column (Column) : container for generic info about the column of that cell
    Returns:
        is_na (bool) : whether that cell is a wrongly typed NA 
    """
    missing_values = ["n/a", "na", "--", "-"]

    if cell_str in missing_values: 
        return True
    else:
        return False