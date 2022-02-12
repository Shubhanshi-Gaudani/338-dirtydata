from src import KNearestNeighbors, csvToMatrix
import numpy as np

def _test_model(model, args = tuple(), kwargs = {}):
    mat = csvToMatrix('tests/test_sheet_1.csv')[1:]
    posed = mat.T.tolist()
    for col in range(len(posed) - 1):
        feat_list = posed[:col] + posed[col + 1:]
        feats = np.array(feat_list, dtype = 'U128').T
        targs = np.array(posed[col], dtype = 'U128')
        m = model(*args, **kwargs)
        m.fit(feats, targs)
        for preds in [m.predict(feats, nprocs = 1), m.predict(feats, nprocs = 8)]:
            assert preds.shape == (mat.shape[0],)
            assert preds.dtype == mat.dtype

def test_knn():
    _test_model(KNearestNeighbors, args = (5,))
