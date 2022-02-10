import pandas as pd
import numpy as np

from src.utilities import can_be_float
from .rule_base import RuleBaseClass

_QUANT_SCALE = 2

def _num_is_outlier(x, perc25, perc75, quant_scale = _QUANT_SCALE):
    """Takes a number and returns if it's an outlier."""
    iqr = perc75 - perc25
    return (x < perc25 - quant_scale * iqr or
            x > perc75 + quant_scale * iqr)

class NumOutlier (RuleBaseClass):
    """Checks if cells are numeric outliers."""
    def is_dirty(self, cell_str, col):
        if not can_be_float(cell_str): return False
        return _num_is_outlier(float(cell_str), col.quantile(0.25), col.quantile(0.75))

    def message(self, cell_str, col):
        med = col.quantile(0.5)
        above = 'above' if float(cell_str) > med else 'below'
        return f'This cell was way {above} the median, which was {med}.'

    def clean(self, col):
        return str(col.quantile(0.5))
