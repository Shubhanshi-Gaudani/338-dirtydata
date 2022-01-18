import numpy as np
import pandas as pd
from .utilities import can_be_float

class Column:
    def __init__(self, col):
        self.mean = self.get_mean(col)
        self.stddev = self.get_stddev(col)
        self.median = self.get_median(col)
        self.mode = self.get_mode(col)
        self.column_type = self.get_col_type(col)

    def get_mean(self, col):
        raise NotImplementedError
    
    def get_stddev(self, col):
        std = np.std(col)
        return std;

    def get_median(self, col):
        return np.nanmedian(col)

    def get_mode(self, col):
        raise NotImplementedError

    def get_col_type(self, col):
        """returns the most common column type - either 'num' or 'alpha'."""
        al_num_counts = [0, 0]
        for row in range(col.shape[0]):
            al_num_counts[int(can_be_float(col[row]))] += 1
        typs = ['alpha', 'num']
        return typs[np.argmax(al_num_counts)]
