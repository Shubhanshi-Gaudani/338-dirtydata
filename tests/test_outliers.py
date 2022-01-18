from src import is_outlier, Column, can_be_float

def test_outliers():
    c = Column(0, 1)
    assert is_outlier('10', c)
    assert is_outlier('10.0', c)
    assert is_outlier('aa', c)
    assert not is_outlier('0', c)
    assert not is_outlier('0.0', c)
    assert is_outlier('-10', c)
    assert not is_outlier('-1', c)

def test_can_be_float():
    assert can_be_float('0')
    assert can_be_float('0.0')
    assert can_be_float('-1.0')
    assert can_be_float('-1')
    assert not can_be_float('')
    assert not can_be_float('not a float')