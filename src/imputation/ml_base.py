import multiprocessing as mp
import numpy as np
from itertools import starmap

class MlBase:
    """The abstract base class for machine learning models.
    
    Children need to define __init__, fit, and _pred_one_row functions.
    """
    def __init__(self):
        raise NotImplementedError

    def fit(self, sheet):
        """Trains the model based on features and targets.
        
        Args:
            sheet (np.array) : a 2D array of strings representing
                the entire matrix

        Returns:
            None
        """
        raise NotImplementedError

    def _pred_one_row(self, row, all_dirty):
        """Gathers the prediction for one row of data.
        
        Args:
            row (np.array) : a 1D array of string features
            all_dirty (np.array) : an array of all [y, x] pairs with dirty cells

        Returns:
            pred (str) : the model's prediction
        """
        raise NotImplementedError

    def _predict_seq(self, features, all_dirty):
        """Sequentially gathers the model's predictions for features.
        
        Args:
            features (np.array) : a 2D array of string features
            all_dirty (np.array) : an array of all [y, x] pairs with dirty cells

        Returns:
            preds (np.array) : a 1D array of string predictions
        """
        args = [ (features[i], all_dirty) for i in range(features.shape[0]) ]
        return np.fromiter(starmap(self._pred_one_row, args),
                           dtype = 'U128',
                           count = features.shape[0])

    def _predict_par(self, features, all_dirty, nprocs):
        """Gathers the model's predictions for features in parallel.
        
        Args:
            features (np.array) : a 2D array of string features
            all_dirty (np.array) : an array of all [y, x] pairs with dirty cells
            nprocs (int) : how many processors to use

        Returns:
            preds (np.array) : a 1D array of string predictions
        """
        args = [ (features[i], all_dirty) for i in range(features.shape[0]) ]
        with mp.Pool(nprocs) as pool:
            return np.array(pool.starmap(self._pred_one_row, args), dtype = 'U128')

    def predict(self, features, all_dirty, nprocs = 8):
        """Gathers the model's predictions for features.
        
        Args:
            features (np.array) : a 2D array of string features
            all_dirty (np.array) : an array of all [y, x] pairs with dirty cells
            nprocs (int) : how many processes to use. If 1, no
                processes will be created. Default is 8.

        Returns:
            preds (np.array) : a 1D array of string predictions
        """
        nprocs = min(nprocs, features.shape[0])
        if nprocs > 1:
            return self._predict_par(features, all_dirty, nprocs)
        return self._predict_seq(features, all_dirty)
