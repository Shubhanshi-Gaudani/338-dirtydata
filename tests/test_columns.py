from src import Column
import numpy as np

def _array_args():
    return [np.array(['0', '1', '1.0', '-1.0']),
            np.array(['1', '2', '3', '4', '5']),
            np.array([' ', 'na', '2', 'string', '1', '-100', 'more string'])]

def test_col_mean():
    cols = map(Column, _array_args())
    true_means = [0.25, 3, -32.333]
    means = list(map(lambda c: c.mean, cols))
    assert np.allclose(means, true_means)

def test_col_stddev():
    cols = map(Column, _array_args())
    true_stds = [0.82915, 1.41421, 47.8493]
    stds = list(map(lambda c: c.stddev, cols))
    assert np.allclose(true_stds, stds)

def test_median():
    cols = map(Column, _array_args())
    true_medians = [0.5, 3, 1]
    medians = list(map(lambda c: c.median, cols))
    assert np.allclose(true_medians, medians)

def test_mode():
    # the arrays I've been using aren't great for this problem but
    # I don't want to change them bc then I'd have to change all
    # the other test cases
    cols = [Column(np.array(['0', '2', '-1', '2', '0', '2'])),
            Column(np.array(['1', 'na', ' ', '1', '2', 'string'])),
            Column(np.array(['-1', '-100', '1lbs', '-100']))]
    true_modes = [2, 1, -100]
    modes = list(map(lambda c: c.mode, cols))
    assert np.allclose(true_modes, modes)

def test_col_type():
    cols = map(Column, _array_args())
    true_types = ['num', 'num', 'alpha']
    types = list(map(lambda c: c.column_type, cols))
    for i in range(len(cols)):
        assert true_types[i] == types[i], f'{true_types} != {types}'
        