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

def save_clean(mat, inds, reasons, cols, clean_row = True, clean_columns = True):
    """Cleans mat and saves it to CLEAN_PATH.
    
    Args:
        mat (np.array) : the 2D array of strings to clean
        inds (np.array) : a array of [y, x] pairs that can be used to index into 
            mat
        reasons (np.array) : an array of functions that the cells in 
            dirty failed. reasons[i] is the reason why dirty[i] failed
        cols (list) : a list of Column objects

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
    # duplicate rows 
    if(clean_row):
        dupes = duplicate_row(mat)
        mat = np.delete(mat, dupes, 0)
    # duplicate columns
    if(clean_columns):
        dupes = duplicate_columns(mat)
        mat = np.delete(mat, dupes, 1)

    np.savetxt(CLEAN_PATH, 
               mat, 
               fmt = '%s', 
               delimiter = ',', 
               encoding = 'utf-8')
