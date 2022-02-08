from src import all_dirty_cells, user_message, csvToMatrix

if __name__ == '__main__':
    mat = csvToMatrix('tests/test_sheet_1.csv')
    inds, reasons, cols = all_dirty_cells(mat, header = 1, parallel = False, return_cols = True)

    for i in range(inds.shape[0]):
        true_inds = (inds[i, 0] + 1, inds[i, 1])
        print(f'Cell {true_inds[1] + 1} in row {mat[true_inds[0]]} is dirty.\n' +
              user_message(mat[true_inds], 
                           cols[true_inds[1]], 
                           reasons[i]) +
              '\n')
