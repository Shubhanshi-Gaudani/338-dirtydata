from src import is_outlier, Column, is_na, isIncorrectDataType, missing_data
import numpy as np

def _def_col():
    return Column(np.array(['0', '1', '-1']))

def test_outliers():
    c = _def_col
    assert is_outlier('10', c)
    assert is_outlier('10.0', c)
    assert is_outlier('aa', c)
    assert not is_outlier('0', c)
    assert not is_outlier('0.0', c)
    assert is_outlier('-10', c)
    assert not is_outlier('-1', c)

def test_na():
    c = _def_col()
    assert is_na('na', c)
    assert is_na('NA', c)
    assert is_na('Na', c)
    assert is_na('N/A', c)
    assert is_na('n/a', c)
    assert is_na('not applicable', c)
    assert not is_na('real text', c)
    assert not is_na('nan', c)
    assert not is_na('1', c)
    assert not is_na('0.0', c)

def test_correct_dtype():
    c = _def_col()
    assert isIncorrectDataType('string', c)
    assert not isIncorrectDataType('', c)
    assert isIncorrectDataType('1.0', Column(np.array(['string'])))
    assert not isIncorrectDataType('s', Column(np.array(['string'])))
    assert not isIncorrectDataType('1', c)
    assert not isIncorrectDataType('1.0', c)
    assert not isIncorrectDataType('-1.0', c)

def test_missing():
    c = _def_col()
    assert missing_data('', c)
    assert missing_data(' ', c)
    assert missing_data('\t', c)
    assert not missing_data('hello', c)
    assert not missing_data('0', c)
