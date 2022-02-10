import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from sklearn.neighbors import KNeighborsRegressor
from tensorflow import keras
from keras import layers
from keras import models
from keras import losses
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier

_FITTED_MODELS = None
_COL_MODELS = None

def get_models():
    """Returns _FITTED_MODELS, _COL_MODELS (for testing mostly)."""
    return _FITTED_MODELS, _COL_MODELS

def set_models(new_fitted, new_cols):
    """Sets _FITTED_MODELS to new_fitted and _COL_MODELS to new_cols (for testing mostly)."""
    global _FITTED_MODELS, _COL_MODELS
    _FITTED_MODELS = new_fitted
    _COL_MODELS = new_cols

def clean_cell(sheet, inds, col, model_type = 'auto'):
    """Returns a suggested string that could go in the sheet at inds.
    
    Args:
        sheet (np.array) : a 2D array of strings from the input spreadsheet
        inds (np.array) : a [y, x] pair for indexing into the sheet
        col (Column) : a Column object with information about the cell's column
        model_type (str) : what ML model to use to predict the cell. One of 'auto',
            'knn', 'deep', 'deep learning', 'naive bayes'. If 'auto' (the default),
            the model type will be chosen by this function based on the spreadsheet
            and the column.

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    global _COL_MODELS, _FITTED_MODELS
    xs = np.append(sheet[:, :inds[1]], sheet[:, inds[1] + 1:], axis = 1)
    if _COL_MODELS is None:
        set_models(np.zeros(sheet.shape[1], dtype = bool),
                   np.empty(sheet.shape[1], dtype = object))
    if _FITTED_MODELS[inds[1]]:
        model = _COL_MODELS[inds[1]]
    else:
        # people who are better with neural nets, feel free to change me!
        # dl_model = models.Sequential([layers.Dense(16, activation = 'relu'),
        #                               layers.Dense(128, activation = 'relu'),
        #                               layers.Dense(64, activation = 'relu'),
        #                               layers.Dense(1, activation = 'relu')])
        # dl_model.compile(optimizer = 'adam',
        #                  loss = losses.MeanSquaredError(),
        #                  metrics = ['mae'])
        # untrained = {'knn' : KNeighborsRegressor(),
        #              'deep' : dl_model,
        #              'deep learning' : dl_model,
        #              'naive bayes' : GaussianNB()}
        untrained = {'forest' : RandomForestClassifier()}
        if model_type == 'auto':
            if (col.column_type == 'alpha' or
                sheet.shape[0] < 2_000):
                model = untrained['knn']
            else:
                model = untrained['forest']
        else:
            model = untrained[model_type]

        model.fit(xs, sheet[:, inds[1]])
        _COL_MODELS[inds[1]] = model
        _FITTED_MODELS[inds[1]] = True

    return model.predict(xs[inds[0]])[0]
