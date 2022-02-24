from src import all_dirty_cells, csvToMatrix, _ALL_PREDS
from src import MissingData, IsIncorrectDataType, NumOutlier, IsNA, WrongCategory, HasTypo
import numpy as np

ENABLE_NFL = False

def test_dirty_cells():
    mat = csvToMatrix("test_sheets/test_sheet_1.csv")
    has_zero = False
    for row in mat:
        for col in row:
            if col == '':
                has_zero = True
                break
        else:
            continue
        break
    assert has_zero

    inds, reasons = all_dirty_cells(mat, 
                                    header = 1)
    right_inds = np.array([[1, 1],
                           [1, 2],
                           [1, 7],
                           [2, 4],
                           [2, 6],
                           [2, 8],
                           [5, 3],
                           [6, 3],
                           [6, 6],
                           [8, 3],
                           [8, 6]])
    right_reasons = [MissingData,
                     NumOutlier,
                     NumOutlier,
                     HasTypo,
                     IsIncorrectDataType,
                     WrongCategory,
                     IsNA,
                     MissingData,
                     NumOutlier,
                     IsNA,
                     NumOutlier]
    assert right_inds.shape[0] == len(right_reasons)
    assert np.all(inds == right_inds), (inds.shape[0], right_inds.shape[0])
    for i in range(len(right_reasons)):
        if reasons[i] != right_reasons[i]:
            print(i, reasons[i], right_reasons[i])
    assert np.all(reasons == right_reasons)

    seq_inds, seq_reasons = all_dirty_cells(mat, 
                                            header = 1, 
                                            parallel = False,
                                            preds = _ALL_PREDS)
    assert np.all(inds == seq_inds)
    assert np.all(reasons == seq_reasons)
    
def test_with_nfl():
    if ENABLE_NFL:
        mat = csvToMatrix('test_sheets/nfl_data.txt')
        inds, reasons = all_dirty_cells(mat, parallel = False)
    
