from src import can_be_float

def test_can_be_float():
    assert can_be_float('0')
    assert can_be_float('0.0')
    assert can_be_float('-1.0')
    assert can_be_float('-1')
    assert not can_be_float('')
    assert not can_be_float('not a float')
