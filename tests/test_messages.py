from src import user_message, Column
from src import is_outlier, is_na, isIncorrectDataType, missing_data
from src import outlier_message, na_message, incorrect_dtype_message, missing_message
import numpy as np

def test_messages():
    cell_str = 'hello'
    col = Column(np.array(['string1', '2', '3.0', '1.0']))
    assert user_message(cell_str, col, is_na) == na_message(cell_str, col)
    assert user_message(cell_str, col, isIncorrectDataType) == incorrect_dtype_message(cell_str, col)
    assert user_message(cell_str, col, missing_data) == missing_message(cell_str, col)
    num_col = Column(np.array(['1', '-1', '0']))
    assert user_message('10', num_col, is_outlier) == outlier_message('10', num_col)
    