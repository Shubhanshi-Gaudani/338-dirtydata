#Import necessary libraries 
import numpy as np 
import pandas as pd
from .rule_base import RuleBaseClass

class MissingData (RuleBaseClass):
    """Checks if cells are missing/empty."""
    def is_dirty(self, cell_str, col):
        if (cell_str.strip() == ""): 
            return True
        else:
            return False

    def message(self, cell_str, col):
        return 'The cell is empty.'

    def clean(self, inds, sheet, col):
        return col.generic_clean(inds, sheet)
