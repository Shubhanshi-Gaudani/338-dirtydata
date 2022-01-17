from termios import CR0
from src import is_outlier, Column

def test_outliers():
    c = Column(0, 1)
    assert is_outlier('10', c)
    assert is_outlier('10.0', c)
    assert is_outlier('aa', c)
    assert not is_outlier('0', c)
    assert not is_outlier('0.0', c)
    assert is_outlier('-10', c)
    assert not is_outlier('-1', c)