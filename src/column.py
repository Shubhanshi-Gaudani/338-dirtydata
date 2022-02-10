import numpy as np
import pandas as pd
import scipy.stats as sp
import math as math
from .utilities import can_be_float, can_be_int
from .rules import IsNA
from Levenshtein import distance

_COUNT_PER_100_LINES = 3

class Column:
    def __init__(self, col):
        """A container class for a bunch of information specific to a column of data.
        
        Args:
            col (np.array) : a numpy array of strings containing the data
        """
        self.length = col.shape[0]
        self.str_els = self.get_str_els(col)
        self.num_els = self.get_num_els(col)
        self.by_count = self.get_by_count(col)
        self.counts_over_thresh = self.get_counts_over_thresh(col)
        self.mean = self.get_mean(col)
        self.stddev = self.get_stddev(col)
        self._quants = self.get_quants(col)
        self.median = self.quantile(0.5)
        self.mode = self.get_mode(col)
        self.column_type = self.get_col_type(col)

    def get_counts_over_thresh(self, col):
        """Returns the number of elements in col with more than _COUNTS_PER_100_LINES occurences per 100 lines.
        
        Args:
            col (np.array) : an array of strings

        Returns:
            num_over (int) : the number of categories in col
        """
        res = 0
        for el in self.by_count:
            count = self.by_count[el]
            if self.length > 100:
                count = 100 * count / self.length
            res += int(count >= _COUNT_PER_100_LINES)
        return res

    def get_str_els(self, col):
        """Returns all the non-numerical elements in col.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            str_els (np.array) : the non-numerical elements
        """
        return np.array([ el for el in col if not can_be_float(el) ], dtype = str)

    def get_num_els(self, col):
        """Returns all numerical elements in col.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            num_els (np.array) : the numerical elements, all cast as float      
        """
        return np.array([ float(el) for el in col if can_be_float(el) and not np.isnan(float(el)) ])

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
        if self.num_els.shape[0] == 0: return np.nan
        return np.mean(self.num_els)
    
    def get_stddev(self, col):
        """Returns the standard deviation of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            stddev (float) : the standard deviation of the numeric cells in col
        """
        if self.num_els.shape[0] == 0: return np.nan
        return np.std(self.num_els)

    def get_median(self, col):
        """Returns the median of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            median (float) : the median of the numeric cells in col
        """
        if self.num_els.shape[0] == 0: return np.nan
        return np.median(self.num_els)

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
            if not IsNA().is_dirty(el, None):
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
            quants (list) : a list of floats corresponding to different quantiles
        """
        qs = np.array([0, 0.25, 0.5, 0.75, 1])
        if self.num_els.shape[0] == 0: return [np.nan] * qs.shape[0]
        return [ np.quantile(self.num_els, q) for q in qs ]

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
        """Returns the most common column type - either 'int', 'float', or 'alpha'.
        
        Args:
            col (np.array) : an array of strings
            
        Returns:
            type (string) : either 'int', 'float', or 'alpha'
        """
        if self.str_els.shape[0] >= self.num_els.shape[0]:
            return 'alpha'
        counts = [0, 0]
        for el in col:
            if can_be_int(el):
                counts[0] += 1
            elif can_be_float(el):
                counts[1] += 1
        typs = ['int', 'float']
        return typs[np.argmax(counts)]

    def get_by_count(self, col):
        """Returns a dictionary mapping the elements in col to how often they occur in col.
        
        Args:
            col (np.array) : an array of strings

        Returns:
            by_count (dict) : a mapping from string element to the count of that element in col
        """
        res = {}
        for el in col:
            res[el] = res[el] + 1 if el in res else 1

        return res
