import numpy as np
from Levenshtein import distance
from ..rules import IsNA

def tolerant_euc(x, y):
    """Returns the euclidean distance between possible dirty arrays.

    Note that, for efficiency reasons, this returns the square of the 
    euclidean distance between x and y
    
    Args:
        x (np.array) : a 1D array of string features
        y (np.array) : a 1D array of string features

    Returns:
        dist (float) : the squared distance between the two
    """
    nan_checker = IsNA()
    res = 0
    for i in range(min(x.shape[0], y.shape[0])):
        if (x[i] and 
            y[i] and 
            not nan_checker.is_dirty(x[i], None) and
            not nan_checker.is_dirty(y[i], None)):
            try:
                res += (float(x[i]) - float(y[i])) ** 2
            except ValueError:
                res += distance(x[i], y[i])

    return res
