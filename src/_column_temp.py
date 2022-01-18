import numpy as np
import pandas as pd

class Column:
    """Temporary container class for column data.
    
    Put any information your predicates need about the columns in
    this class and we can write some code to analyze the data to find
    that information later
    """
    def __init__(self):
        self.mean = np.nan
        self.stddev = np.nan
        self.column_type = ''