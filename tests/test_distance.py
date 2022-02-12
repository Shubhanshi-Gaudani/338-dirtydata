from src import tolerant_euc
import numpy as np
from Levenshtein import distance

def test_euc():
    arr1 = np.array(['1', '2', '3', '4'])
    arr2 = np.array(['3', '4', '5', '6'])
    assert tolerant_euc(arr1, arr2) == 16
    arr3 = np.array(['1', '2', '', '4'])
    assert tolerant_euc(arr2, arr3) == 12
    arr4 = np.array(['string', '2', '3', '4'])
    assert tolerant_euc(arr2, arr4) == 12 + distance('1', 'string')
    arr5 = np.array(['5', '6', 'nan', ''])
    assert tolerant_euc(arr1, arr5) == 32
