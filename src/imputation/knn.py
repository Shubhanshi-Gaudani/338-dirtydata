import numpy as np
from .ml_base import MlBase
from .distance import tolerant_euc
from ..rules import IsNA

class KNearestNeighbors (MlBase):
    """Aggregates predictions from the k nearest neighbors to each row of features.
    
    Args:
        k (int) : how many neighbors to look at per row
    """
    def __init__(self, k):
        self.k = k
        self.features = None
        self.targets = None
        self.nan_checker = IsNA()

    def fit(self, features, targets):
        self.features = features
        self.targets = targets

    def _mode(self, X):
        """Returns the most common element in X."""
        counts = {}
        for el in X:
            if el and not self.nan_checker.is_dirty(el, None):
                counts[el] = counts[el] + 1 if el in counts else 1
        if len(counts):
            return max(counts, key = counts.__getitem__)
        return ''

    def _pred_one_row(self, row):
        dists = sorted(range(self.features.shape[0]),
                       key = lambda i: tolerant_euc(row, self.features[i]))
        k_targs = dists[1:self.k + 1]
        return self._mode(self.targets[k_targs])
