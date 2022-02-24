import numpy as np
from .csv_to_matrix import has_header
from .utilities import arr_to_set
import multiprocessing as mp
from itertools import starmap

_NPROCS = 8

def clean_cell(inds, sheet, col, reason, all_dirty):
    """Uses a dumber but simpler model for imputing cell type.
    
    Args:
        inds (np.array) : a [y, x] pair indicating which cell to clean
        sheet (np.array) : a 2D matrix of strings.
            If there is a header, it should have been skipped already
        col (Column) : a container class with information about the cell's column
        reason (function) : a predicate representing why the cell is dirty
        all_dirty (set) : a set of [y, x] pairs indicating all the cells that are dirty

    Returns:
        predicted (str) : what the model predicts should go in that cell
    """
    return reason().clean(inds, sheet, col, all_dirty)

def clean_all_cells(mat, inds, reasons, cols):
    """Cleans all the cells. 
    
    Mat does not need to have the header skipped and inds can be a list.
    
    Args:
        mat (np.array) : a 2D array of strings
        inds (np.array) : an array of [y, x] pairs corresponding to dirty
            cells in mat
        reasons (list) : a list of RuleBase types indicating why each cell is dirty
        cols (list) : a list of Column objects

    Returns:
        suggs (np.array) : a 1D array of strings for suggested imputations
    """
    skip = has_header(mat)
    mat2 = mat[skip:]
    real_inds = np.array([ [inds[i, 0] - skip, inds[i, 1]] for i in range(inds.shape[0]) ])
    s_inds = arr_to_set(inds)
    nprocs = min(_NPROCS, inds.shape[0])
    args = []
    for i in range(inds.shape[0]):
        args.append((real_inds[i], mat2, cols[real_inds[i, 1]], reasons[i], s_inds))
    with mp.Pool(nprocs) as pool:
        return np.array(pool.starmap(clean_cell, args), dtype = 'U128')
    # return np.fromiter(starmap(clean_cell, args), dtype = 'U128', count = len(args))
