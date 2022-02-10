import numpy as np
from pyparsing import col

_COUNT_PER_100_LINES = 2
_NUM_CATS_PER_100 = 2

def wrong_cat(cell_str, column):
    """Takes the string version of the cell and returns if it is unlike other categories.

    Args:
        cell_str (str) : the raw text of that cell
        column (Column) : container for generic info about the column of that cell

    Returns:
        is_wrong_cat (bool) : whether cell_str is not one of a small amount of categories in column
    """
    counts = column.by_count[cell_str]
    cats = column.counts_over_thresh
    if column.length > 100:
        per_100 = lambda n: 100 * n / column.length 
        counts = per_100(counts)
        cats = per_100(cats)

    return counts <= _COUNT_PER_100_LINES and cats >= _NUM_CATS_PER_100

def wrong_cat_message(cell_str, col):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the column

    Returns:
        message (str) : a readable reason why the string was dirty
    """
    return ('This row appears to have a small number of categories, but ' +
            f'{cell_str} is not one of them.')

def clean_wrong_cat(col):
    """Returns the desired imputed value based on data from col.
    
    Args:
        col (Column) : a container class with information about the cell's column

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    return str(col.mode)

