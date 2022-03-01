from src import duplicate_row, duplicate_columns, csvToMatrix, redundant_columns

_SHEET_NAME = 'test_sheets/test_sheet_1.csv'

def test_dupe_rows():
    mat = csvToMatrix(_SHEET_NAME)
    dupes = duplicate_row(mat)
    assert dupes == [7]

def test_dupe_cols():
    mat = csvToMatrix(_SHEET_NAME)
    dupes = duplicate_columns(mat)
    assert dupes == [7]

def test_red_cols():
    mat = csvToMatrix(_SHEET_NAME)
    reds = redundant_columns(mat)
    real_reds = [(0, 1),
                 (0, 4),
                 (0, 6),
                 (2, 7),
                 (8, 9)]
    assert reds == real_reds
