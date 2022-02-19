import multiprocessing as mp
import numpy as np

class MlBase:
    """The abstract base class for machine learning models.
    
    Children need to define __init__, fit, and _pred_one_row functions.
    """
    def __init__(self):
        raise NotImplementedError

    def fit(self, features, targets):
        """Trains the model based on features and targets.
        
        Args:
            features (np.array) : a 2D array of string features
            targets (np.array) : a 1D array of string targets

        Returns:
            None
        """
        raise NotImplementedError

    def _pred_one_row(self, row):
        """Gathers the prediction for one row of data.
        
        Args:
            row (np.array) : a 1D array of string features

        Returns:
            pred (str) : the model's prediction
        """
        raise NotImplementedError

    def _predict_seq(self, features):
        """Sequentially gathers the model's predictions for features.
        
        Args:
            features (np.array) : a 2D array of string features

        Returns:
            preds (np.array) : a 1D array of string predictions
        """
        return np.fromiter(map(self._pred_one_row, features),
                           dtype = 'U128',
                           count = features.shape[0])

    def _predict_par(self, features, nprocs):
        """Gathers the model's predictions for features in parallel.
        
        Args:
            features (np.array) : a 2D array of string features
            nprocs (int) : how many processors to use

        Returns:
            preds (np.array) : a 1D array of string predictions
        """
        with mp.Pool(nprocs) as pool:
            return np.array(pool.map(self._pred_one_row, features), dtype = 'U128')

    def predict(self, features, nprocs = 8):
        """Gathers the model's predictions for features.
        
        Args:
            features (np.array) : a 2D array of string features
            nprocs (int) : how many processes to use. If 1, no
                processes will be created. Default is 8.

        Returns:
            preds (np.array) : a 1D array of string predictions
        """
        nprocs = min(nprocs, features.shape[0])
        if nprocs > 1:
            return self._predict_par(features, nprocs)
        return self._predict_seq(features)
