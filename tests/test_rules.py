from src import is_outlier, Column, is_na, isIncorrectDataType, missing_data, str_outlier, is_email
import numpy as np

def _def_col():
    return Column(np.array(['0', '1', '-1']))

def test_outliers():
    c = _def_col()
    assert is_outlier('10', c)
    assert is_outlier('10.0', c)
    assert not is_outlier('aa', c)
    assert not is_outlier('0', c)
    assert not is_outlier('0.0', c)
    assert is_outlier('-10', c)
    assert not is_outlier('-1', c)

def test_na():
    c = _def_col()
    assert c.mean == 0
    assert is_na('na', c)
    assert is_na('NA', c)
    assert is_na('Na', c)
    assert is_na('N/A', c)
    assert is_na('n/a', c)
    assert is_na('not applicable', c)
    assert not is_na('real text', c)
    assert is_na('nan', c)
    assert not is_na('1', c)
    assert not is_na('0.0', c)

def test_correct_dtype():
    c = _def_col()
    assert c.column_type == 'int'
    assert isIncorrectDataType('string', c)
    assert isIncorrectDataType('1.0', Column(np.array(['string'])))
    assert not isIncorrectDataType('s', Column(np.array(['string'])))
    assert not isIncorrectDataType('1', c)
    assert isIncorrectDataType('1.0', c)
    assert isIncorrectDataType('-1.0', c)
    assert not isIncorrectDataType('1.0', Column(np.array(['0.0', '1.0'])))

def test_missing():
    c = _def_col()
    assert missing_data('', c)
    assert missing_data(' ', c)
    assert missing_data('\t', c)
    assert not missing_data('hello', c)
    assert not missing_data('0', c)

def test_str_outliers():
    if False:
        col = Column(np.array(['abbcc', 'baccd', 'abdcc']))
        assert str_outlier('string', col)
        assert not str_outlier('d', col)
        assert str_outlier('1/21/2022', Column(np.array(['1-21-2022', '1-20-2022', '4-16-2021'])))
        assert not str_outlier('1/21/2022', Column(np.array(['1/21/2022', '1/20/2022', '4/16/2021'])))

def test_is_email():
    col = Column(np.array(['simran@gmail.com', 'yamini@u.northwestern.edu', 'simg@u.northwestern.edu']))
    assert is_email('abc@gmail.com', col)
    assert not is_email('123', col )
    assert not is_email('random_string', col)
    assert is_email('s@nu.northwestern.edu', col)
    assert not is_email('27.5', col)
    assert not is_email('hello@xx', col)

def test_whitesp():
    #this is terribly written code, sorry 🙈
    from src.strip_whitespaces import clean_whitespaces
    col = Column(np.array(['   string', 'hello', '    what da dog doin   ']))
    x = np.array(['   string', 'hello', '    what da dog doin   '])
    y = np.array(['123', '  twentytwo', 'hi my name is  Bob'])
    l = []
    m = []
    for i in x:
        l.append(clean_whitespaces(i, col))
    l = np.array(l)

    for j in y:
        m.append(clean_whitespaces(j,col))
    m = np.array(m)

    assert np.array_equal(l,np.array(['string', 'hello', 'what da dog doin']))
    assert np.array_equal(m, np.array(['123', 'twentytwo', 'hi my name is Bob']))


