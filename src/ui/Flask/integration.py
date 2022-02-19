from src import all_dirty_cells, has_header, clean_cell, duplicate_columns, duplicate_row
from .path_utils import data_path
import numpy as np

CLEAN_NAME = 'cleaned.csv'
CLEAN_PATH = data_path() + '/' + CLEAN_NAME

def get_dirty(mat):
    """Reads mat and finds the dirty cells.
    
    Args:
        mat (np.array) : the 2D array of strings to process

    Returns:
        inds (np.array) : a array of [y, x] pairs that can be used to index into 
            mat
        reasons (np.array) : an array of predicates that the cells in 
            dirty failed. reasons[i] is the reason why dirty[i] failed
        cols (list) : a list of Column objects
    """
    return all_dirty_cells(mat,
                           parallel = True,
                           return_cols = True,
                           header = has_header(mat))

def delete_dupes(mat, del_rows = True, del_cols = True):
    """Deletes duplicate rows and columns.
    
    Args:
        mat (np.array) : a 2D array of strings
        del_rows (bool) : whether to delete duplicate rows. Default is True
        del_cols (bool) : whether to delete duplicate columns. Default is True.

    Returns:
        None
    """
    # duplicate rows 
    if(del_rows):
        dupes = duplicate_row(mat)
        mat = np.delete(mat, dupes, 0)
    # duplicate columns
    if(del_cols):
        dupes = duplicate_columns(mat)
        mat = np.delete(mat, dupes, 1)

def save_clean(mat, inds, reasons, cols, clean_row = True, clean_columns = True):
    """Cleans mat and saves it to CLEAN_PATH.
    
    Args:
        mat (np.array) : the 2D array of strings to clean
        inds (np.array) : a array of [y, x] pairs that can be used to index into 
            mat
        reasons (np.array) : an array of functions that the cells in 
            inds failed. reasons[i] is the reason why inds[i] failed
        cols (list) : a list of Column objects
        clean_row (bool) : whether to remove duplicate rows. Default is True
        clean_columns (bool) : whether to remove duplicate columns. Default is True

    Returns:
        None
    """
    suggs = np.empty(inds.shape[0], dtype = 'U128')
    for i in range(suggs.shape[0]):
        suggs[i] = clean_cell(inds[i],
                              mat,
                              cols[inds[i, 1]],
                              reasons[i])
        mat[tuple(inds[i])] = suggs[i]

    np.savetxt(CLEAN_PATH, 
               mat, 
               fmt = '%s', 
               delimiter = ',', 
               encoding = 'utf-8')
