from src import duplicate_row, duplicate_columns, csvToMatrix

def test_dupe_rows():
    mat = csvToMatrix('test_sheets/test_sheet_1.csv')
    dupes = duplicate_row(mat)
    assert 7 in dupes

def test_dupe_cols():
    mat = csvToMatrix('test_sheets/test_sheet_1.csv')
    dupes = duplicate_columns(mat)
    assert 7 in dupes
