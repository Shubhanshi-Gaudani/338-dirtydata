import numpy as np
import pandas as pd
import scipy.stats as sp
import math as math
from .utilities import can_be_float, can_be_int
from .handle_na import is_na
from Levenshtein import distance

class Column:
    def __init__(self, col):
        """A container class for a bunch of information specific to a column of data.
        
        Args:
            col (np.array) : a numpy array of strings containing the data
        """
        self.mean = self.get_mean(col)
        self.stddev = self.get_stddev(col)
        self._quants = self.get_quants(col)
        self.median = self.quantile(0.5)
        self.mode = self.get_mode(col)
        self.column_type = self.get_col_type(col)
        self.str_els = self.get_str_els(col)
        self.lev_quants = self.get_lev_quants(col)

    def get_str_els(self, col):
        """Returns all the non-numerical elements in col.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            str_els (np.array) : the non-numerical elements
        """
        is_str = np.fromiter(map(can_be_float, col), 
                             dtype = bool, 
                             count = col.shape[0])
        return col[np.invert(is_str)]

    def get_lev_quants(self, col):
        """Returns all the average pairwise hamming distance in col.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            avg_ham (float) : the average hamming distance
        """
        levs = []
        for row in range(self.str_els.shape[0]):
            for row2 in range(1 + row, self.str_els.shape[0]):
                levs.append(distance(self.str_els[row],
                                     self.str_els[row2]))
        
        qs = np.array([0, 0.25, 0.5, 0.75, 1])
        if len(levs) == 0: return [np.nan] * qs.shape[0]
        return [ np.quantile(levs, q) for q in qs ]

    def get_mean(self, col):
        """Returns the mean of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            mean (float) : the mean of the numeric cells in col
        """
        nums = []
        for row in col:
            try:
                nums.append(float(row))
            except ValueError:
                pass
        if len(nums) == 0: return np.nan
        return np.nanmean(nums)
    
    def get_stddev(self, col):
        """Returns the standard deviation of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            stddev (float) : the standard deviation of the numeric cells in col
        """
        sd = 0
        num = 0
        for row in range(col.shape[0]):
            if can_be_float(col[row]) and not np.isnan(float(col[row])):
                sd += (float(col[row]) - self.mean) ** 2
                num += 1
        if num == 0: return 0
        sd = math.sqrt(sd/num)
        return sd

    def get_median(self, col):
        """Returns the median of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            median (float) : the median of the numeric cells in col
        """
        nums = []
        for row in col:
            try:
                nums.append(float(row))
            except ValueError:
                pass
        if len(nums) == 0: return np.nan
        return np.nanmedian(nums)

    def get_mode(self, col):
        """Returns the mode of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            mode (any) : the mode of the cells in col
        """
        counts = {}
        for el in col:
            if not is_na(el, None):
                if el in counts:
                    counts[el] += 1
                else:
                    counts[el] = 1
        return max(counts, key = counts.__getitem__)

    def get_quants(self, col):
        """Returns the 0th, 0.25th, 0.5th, 0.75th, and 1st quantile of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            quants (float) : the IQR of the numeric cells in col
        """
        nums = []
        for row in col:
            try:
                if not is_na(row, None):
                    nums.append(float(row))
            except ValueError:
                pass
        qs = np.array([0, 0.25, 0.5, 0.75, 1])
        if len(nums) == 0: return [np.nan] * qs.shape[0]
        return [ np.quantile(nums, q) for q in qs ]

    def quantile(self, q):
        """Returns the qth quantile. Quantile must be in [0, 0.25, 0.5, 0.75, 1].
        
        Args:
            q (float) : the quantile to return. Must be one of 0, 0.25, 0.5, 0.75, 1

        Returns:
            quant (float) : the qth quantile of the column
        """
        assert q in {0, 0.25, 0.5, 0.75, 1}, f'unsupported value for quantile : {q}'
        return self._quants[int(4 * q)]

    def get_col_type(self, col):
        """Returns the most common column type - either 'num' or 'alpha'.
        
        Args:
            col (np.array) : an array of strings
            
        Returns:
            type (string) : either 'num' or 'alpha'
        """
        al_num_counts = [0, 0, 0]
        for row in col:
            if not is_na(row, None):
                if can_be_int(row):
                    al_num_counts[1] += 1
                elif can_be_float(row):
                    al_num_counts[2] += 1
                else:
                    al_num_counts[0] += 1
        typs = ['alpha', 'int', 'float']
        return typs[np.argmax(al_num_counts)]
