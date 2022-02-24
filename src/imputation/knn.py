import numpy as np
from .ml_base import MlBase
from .distance import tolerant_euc
from ..rules import IsNA

class KNearestNeighbors (MlBase):
    """Aggregates predictions from the k nearest neighbors to each row of features.
    
    Args:
        k (int) : how many neighbors to look at per row
        row_ind (int) : what index the target column is in
    """
    def __init__(self, k, row_ind):
        self.k = k
        self.features = None
        self.targets = None
        self.row_ind = row_ind

    def fit(self, features, targets):
        self.features = features
        self.targets = targets

    def _mode(self, X):
        """Returns the most common element in X."""
        counts = {}
        for el in X:
            counts[el] = counts[el] + 1 if el in counts else 1
        if len(counts):
            return max(counts, key = counts.__getitem__)
        return ''

    def _pred_one_row(self, row, all_dirty):
        inds = filter(lambda i: (i, self.row_ind) not in all_dirty, 
                      range(self.features.shape[0]))
        dists = sorted(inds,
                       key = lambda i: tolerant_euc(row, self.features[i]))
        k_targs = dists[1:min(self.k + 1, len(dists))]
        return self._mode(self.targets[k_targs])
