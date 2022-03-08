import numpy as np
from .ml_base import MlBase
from ..rules import IsNA
from Levenshtein import distance

class KNearestNeighbors (MlBase):
    """Aggregates predictions from the k nearest neighbors to each row of features.
    
    Args:
        k (int) : how many neighbors to look at per row
        row_ind (int) : what index the target column is in
        header (int) : how many rows the original matrix in the header. Default is 1
    """
    def __init__(self, k, col_ind):
        self.k = k
        self.sheet = None
        self.col_ind = col_ind
        self.nan_checker = IsNA()

    def fit(self, sheet):
        self.sheet = sheet

    def _mode(self, X):
        """Returns the most common element in X."""
        counts = {}
        for el in X:
            counts[el] = counts[el] + 1 if el in counts else 1
        if len(counts):
            return max(counts, key = counts.__getitem__)
        return ''

    def _pred_one_row(self, row, all_dirty):
        inds = filter(lambda i: (i, self.col_ind) not in all_dirty, 
                      range(self.sheet.shape[0]))
        dists = sorted(inds,
                       key = lambda i: self._tolerant_euc(row, self.sheet[i]))
        k_targs = dists[1:min(self.k + 1, len(dists))]
        return self._mode(self.sheet[k_targs, self.col_ind])

    def _tolerant_euc(self, x, y):
        """Returns the euclidean distance between possible dirty arrays.

        Note that, for efficiency reasons, this returns the square of the 
        euclidean distance between x and y
        
        Args:
            x (np.array) : a 1D array of string features
            y (np.array) : a 1D array of string features

        Returns:
            dist (float) : the squared distance between the two
        """
        res = 0
        for i in range(min(x.shape[0], y.shape[0])):
            if (i != self.col_ind and
                x[i] and 
                y[i] and 
                not self.nan_checker.is_dirty(x[i], None) and
                not self.nan_checker.is_dirty(y[i], None)):
                try:
                    res += (float(x[i]) - float(y[i])) ** 2
                except ValueError:
                    res += distance(x[i], y[i])

        return res
