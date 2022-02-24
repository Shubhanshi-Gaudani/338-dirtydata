from src import all_dirty_cells, has_header, duplicate_columns, duplicate_row, clean_all_cells
from .path_utils import config_file_path, CLEAN_NAME, CLEAN_PATH
import numpy as np
from src import IsNA, IsIncorrectDataType, MissingData, NumOutlier, WrongCategory, HasTypo, EmailChecker
from src import _ALL_PREDS

DUP_ROW_IND = 0
DUP_COL_IND = 1

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
        mat (np.array) : the possibly changed sheet to clean
    """
    preds, dups = get_preds()
    mat = delete_dupes(mat, 
                       del_rows = dups[DUP_ROW_IND],
                       del_cols = dups[DUP_COL_IND])
    return all_dirty_cells(mat,
                           parallel = True,
                           return_cols = True,
                           header = has_header(mat),
                           preds = preds) + (mat,)

def delete_dupes(mat, del_rows = True, del_cols = True):
    """Deletes duplicate rows and columns.
    
    Args:
        mat (np.array) : a 2D array of strings
        del_rows (bool) : whether to delete duplicate rows. Default is True
        del_cols (bool) : whether to delete duplicate columns. Default is True.

    Returns:
        new_mat (np.array) : the updated matrix
    """
    # duplicate rows 
    if(del_rows):
        dupes = duplicate_row(mat)
        mat = np.delete(mat, dupes, 0)
    # duplicate columns
    if(del_cols):
        dupes = duplicate_columns(mat)
        mat = np.delete(mat, dupes, 1)
    
    return mat

def save_clean(mat, inds, reasons, cols):
    """Cleans mat and saves it to CLEAN_PATH.
    
    Args:
        mat (np.array) : the 2D array of strings to clean
        inds (np.array) : a array of [y, x] pairs that can be used to index into 
            mat
        reasons (np.array) : an array of functions that the cells in 
            inds failed. reasons[i] is the reason why inds[i] failed
        cols (list) : a list of Column objects

    Returns:
        None
    """
    suggs = clean_all_cells(mat, inds, reasons, cols)
    for i in range(suggs.shape[0]):
        mat[tuple(inds[i])] = suggs[i]

    np.savetxt(CLEAN_PATH, 
               mat, 
               fmt = '%s', 
               delimiter = ',', 
               encoding = 'utf-8')

def pred_names_to_objs(names):
    """Turns a list of predicate names (as returned by config) into the rules to use.
    
    Args:
        names (list) : a list of string names to use. Technically can be any iterable

    Returns:
        preds (list) : a list of rules to use when finding dirty cells
        dup_lst (list) : a list of booleans, corresponding to whether the user
            wants to delete duplicate rows and columns
    """
    mapping = {IsNA : 'checkNA',
               IsIncorrectDataType : 'IsIncorrectDataType',
               MissingData : 'MissingData',
               NumOutlier : 'NumOutlier',
               WrongCategory : 'WrongCategory',
               HasTypo : 'typo',
               EmailChecker : 'EmailChecker'}
    name_set = set(names)
    res = []
    for pred in _ALL_PREDS:
        if mapping[pred] in name_set:
            res.append(pred)

    dupes = ['DuplicateRows', 'DuplicateColumns']
    dup_lst = [ el in name_set for el in dupes ]
    return res, dup_lst

def get_preds():
    """Returns the user's selected predicates."""
    with open(config_file_path(), 'r') as config:
        lines = config.readlines()
    for line in range(len(lines)):
        lines[line] = lines[line].replace('\n', '')
    return pred_names_to_objs(lines)
