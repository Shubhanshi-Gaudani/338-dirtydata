import numpy as np
import pandas as pd
import scipy as sp
from .utilities import can_be_float

class Column:
    def __init__(self, col):
        """A container class for a bunch of information specific to a column of data.
        
        Args:
            col (np.array) : a numpy array of strings containing the data
        """
        self.mean = self.get_mean(col)
        self.stddev = self.get_stddev(col)
        self.median = self.get_median(col)
        self.mode = self.get_mode(col)
        self.column_type = self.get_col_type(col)

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
        return np.nanmean(nums)
    
    def get_stddev(self, col):
        """Returns the standard deviation of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            stddev (float) : the standard deviation of the numeric cells in col
        """
        std = np.std(col)
        return std

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
        return np.nanmedian(nums)

    def get_mode(self, col):
        """Returns the mode of the column.
        
        Args:
            col (np.array) : an array of strings, some of which might be
                numeric, some of which might not
                
        Returns:
            mode (float) : the mode of the cells in col
        """
        return sp.mode(col, nan_policy = "omit")

    def get_col_type(self, col):
        """Returns the most common column type - either 'num' or 'alpha'.
        
        Args:
            col (np.array) : an array of strings
            
        Returns:
            type (string) : either 'num' or 'alpha'
        """
        al_num_counts = [0, 0]
        for row in range(col.shape[0]):
            al_num_counts[int(can_be_float(col[row]))] += 1
        typs = ['alpha', 'num']
        return typs[np.argmax(al_num_counts)]
