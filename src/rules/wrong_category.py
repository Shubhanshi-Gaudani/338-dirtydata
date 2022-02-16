import numpy as np
from .rule_base import RuleBaseClass

_COUNT_PER_100_LINES = 2
_NUM_CATS_PER_100 = 2

class WrongCategory (RuleBaseClass):
    """Checks if a cell is different from the most common categories."""
    def is_dirty(self, cell_str, col):
        counts = col.by_count[cell_str]
        cats = col.counts_over_thresh
        if col.length > 100:
            per_100 = lambda n: 100 * n / col.length 
            counts = per_100(counts)
            cats = per_100(cats)

        return counts <= _COUNT_PER_100_LINES and cats >= _NUM_CATS_PER_100

    def message(self, cell_str, col):
        return ('This row appears to have a small number of categories, but ' +
                f'{cell_str} is not one of them.')

