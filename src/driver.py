import numpy as np
from .csv_to_matrix import csvToMatrix, has_header
import multiprocessing as mp
from itertools import starmap
from .rules import NumOutlier, IsNA, IsIncorrectDataType, MissingData, WrongCategory
from .rules import HasTypo, EmailChecker, duplicate_row, duplicate_columns, user_message, redundant_columns
from .column import Column
from .utilities import arr_to_set, excel_inds, excel_range
import pandas as pd
import xlwings as xw
from .path_utils import CLEAN_XL_PATH
import os

_ALL_PREDS = [MissingData, IsNA, EmailChecker, IsIncorrectDataType, NumOutlier, HasTypo, WrongCategory]

class Driver:
    """The class responsible for finding dirty cells and cleaning them.
    
    Args:
        sheet_path (str) : a path to the matrix to read
        preds (list | None) : a list of predicates to use. If None (the default), it will use all of them
        dupes (list) : a list of Booleans, with the first corresponding to whether to remove duplicate
            rows, the second for duplicate columns, the third for redundant columns. The default is True for 
            first two and false for the last.

    Fields:
        old_mat (np.array) : the user's uploaded spreadsheet, WITHOUT the header if one is present.
            After the header and duplicates are removed, this is read-only
        header (int) : how many rows to skip at the top of the spreadsheet. Typically either 0 or 1
        clean_mat (np.array) : the cleaned version of the user's spreadsheet, WITH the header if one
            is present. Make sure to call clean_all_cells() before using this
        cols (list) : a list of Column objects, one for each column in the user's spreadsheet
        all_preds (list) : a list of types derived from RuleBase which indicate what to use when finding
            dirty cells
        dirty_inds (np.array) : an array of [y, x] pairs to be used to index into old_mat. As such, they will
            not include the header
        s_inds (set) : a set of tuples with the same indices as inds_with_head
        inds_with_head (np.array) : an array of [y, x] pairs to be used to index into clean_mat. They do include
            the header
        reasons (np.array) : an array of types derived from RuleBase. reasons[i] is the reason why the cell at
            dirty_inds[i] is dirty
    """
    def __init__(self, path, preds = None, dupes = [True, True, False]):
        self.old_mat = csvToMatrix(path)
        self.header = has_header(self.old_mat)
        self._del_dupes(dupes[0], dupes[1], dupes[2])
        self.clean_mat = self.old_mat.copy()
        self.old_mat = self.old_mat[self.header:]
        self.cols = None
        self._col_list()

        if preds is None:
            self.all_preds = _ALL_PREDS
        else:
            self.all_preds = preds
        self.preds_inited = [ p() for p in self.all_preds ]

        self.dirty_inds = None
        self.s_inds = None
        self.inds_with_head = None
        self.reasons = None

    def _del_dupes(self, del_rows, del_cols, red_cols):
        """Deletes duplicate rows if del_rows and duplicate columns if del_cols. Saves res to self.old_mat."""
        # duplicate rows 
        if(del_rows):
            dupes = duplicate_row(self.old_mat)
            self.old_mat = np.delete(self.old_mat, dupes, 0)
        # duplicate columns
        if(del_cols):
            dupes = duplicate_columns(self.old_mat)
            self.old_mat = np.delete(self.old_mat, dupes, 1)
        
        # redundant columns
        if(red_cols):
            red_pairs = redundant_columns(self.old_mat)
            red = [a[1] for a in red_pairs]
            self.old_mat = np.delete(self.old_mat, red, 1)

    def _col_list(self, nprocs = 8):
        """Analyzes each column into Column objects and sets self.cols."""
        mat_t = self.old_mat.T
        args = [ (mat_t[i], i) for i in range(mat_t.shape[0]) ]
        nprocs = min(nprocs, mat_t.shape[0])
        if nprocs > 1:
            with mp.Pool(nprocs) as pool:
                self.cols = pool.starmap(Column, args, chunksize = mat_t.shape[0] // nprocs)
        else:
            self.cols = list(starmap(Column, args))

    def _dirty_row(self, row):
        """Worker function for all_dirty_cells"""
        new_row = [None] * len(row)
        for col in range(len(row)):
            for pred in range(len(self.preds_inited)):
                if self.preds_inited[pred].is_dirty(row[col], self.cols[col]):
                    new_row[col] = self.all_preds[pred]
                    break
        return new_row

    def find_dirty_cells(self, nprocs = 8):
        """Finds the indices and reasons for every dirty cell and sets self.inds and self.reasons."""
        nprocs = min(nprocs, self.old_mat.shape[0])

        if nprocs > 1:
            with mp.Pool(nprocs) as pool:
                is_dirty = np.array(pool.map(self._dirty_row, self.old_mat), dtype = object)
        else:
            is_dirty = np.array(list(map(self._dirty_row, self.old_mat)), dtype = object)

        not_none = is_dirty != None
        self.dirty_inds = np.argwhere(not_none)
        self.reasons = is_dirty[not_none]

        self.inds_with_head = self.dirty_inds.copy()
        for i in range(self.dirty_inds.shape[0]):
            self.inds_with_head[i, 0] += self.header
        self.s_inds = arr_to_set(self.inds_with_head)

    def _clean_cell(self, inds, reason):
        """Returns the suggested change to the cell in self.old_mat at inds based on reason."""
        return reason().clean(inds, self.old_mat, self.cols[inds[1]], self.s_inds)

    def _get_suggs(self, nprocs = 1, num_dots = 20):
        """Returns the suggested changes to old_mat."""
        nprocs = min(nprocs, self.dirty_inds.shape[0])
        args = []
        for i in range(self.dirty_inds.shape[0]):
            args.append((self.dirty_inds[i], self.reasons[i]))

        if nprocs > 1:
            with mp.Pool(nprocs) as pool:
                return np.array(pool.starmap(self._clean_cell, 
                                             args, 
                                             chunksize = self.dirty_inds.shape[0] // nprocs), 
                                dtype = 'U128')

        res = np.empty(len(args), dtype = 'U128')
        per_dot = len(args) // num_dots if num_dots else 0
        dot_str = f'|{" " * num_dots}|'
        dot_count = 0
        for i in range(len(args)):
            if per_dot and i % per_dot == 0:
                print(dot_str, end = '\r')
                dot_count += 1
                dot_str = f'|{"." * dot_count}{" " * (num_dots - dot_count)}|'
                
            res[i] = self._clean_cell(*args[i])
        if num_dots: print()
        return res

    def clean_all_cells(self, nprocs = 1, num_dots = 20):
        """Cleans all the cells and saves the changes to self.clean_mat."""
        suggs = self._get_suggs(nprocs = nprocs, num_dots = num_dots)
        for i in range(suggs.shape[0]):
            self.clean_mat[tuple(self.inds_with_head[i])] = suggs[i]
 
    def user_message(self, ind_inds):
        """Returns a user-readable message for the dirty cell at self.old_mat[self.dirty_inds[ind_inds]]."""
        return user_message(self.old_mat[tuple(self.dirty_inds[ind_inds])],
                            self.cols[self.dirty_inds[ind_inds, 1]],
                            self.reasons[ind_inds])

    def save_clean(self, new_pth):
        """Saves self.clean_mat to new_pth."""
        escape_chars = {',', '\n', '"', '\t'}
        for y in range(self.clean_mat.shape[0]):
            for x in range(self.clean_mat.shape[1]):
                for char in self.clean_mat[y, x]:
                    if char in escape_chars:
                        self.clean_mat[y, x] = f'"{self.clean_mat[y, x]}"'
                        break

        np.savetxt(new_pth, 
                   self.clean_mat, 
                   fmt = '%s', 
                   delimiter = ',', 
                   encoding = 'utf-8')

    def save_excel(self):
        """Saves clean_mat to an excel file."""
        pd.DataFrame(self.clean_mat).to_excel(CLEAN_XL_PATH, sheet_name='Sheet1')


    def highlight_excel(self):
        color_dict = {}
        #Define the colours that we want in the highlighted cells:
        #Light Salmon Pink 
        color_dict[MissingData] = (255, 154, 162)
        #Crayola's Periwinkle
        color_dict[IsNA] = (199, 206, 234)
        #Dirty White
        color_dict[NumOutlier] = (226, 240, 203)
        #Phillipine Silver 
        color_dict[HasTypo] = (177, 177, 177)
        #Columbia Blue 
        color_dict[IsIncorrectDataType] = (192, 228, 241)
        #Cookies and Cream
        color_dict[WrongCategory] = (232, 215, 173)
        #Tea Green
        color_dict[EmailChecker] = (208, 246, 210)

        file_name = CLEAN_XL_PATH
        wb = xw.Book(file_name)
        #Name of sheet hardcoded 
        xl_sheet = wb.sheets['Sheet1']
        for i in range(len(self.reasons)):
            cell_str = excel_inds(self.inds_with_head[i])
            xl_sheet.range(excel_range(cell_str)).color = color_dict[self.reasons[i]]
