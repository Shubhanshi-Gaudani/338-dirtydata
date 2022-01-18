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
        raise NotImplementedError

    def get_median(self, col):
        return np.median(col)

    def get_mode(self, col):
        raise NotImplementedError

    def get_col_type(self, col):
        raise NotImplementedError