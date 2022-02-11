from src import all_dirty_cells, user_message, csvToMatrix, clean_cell_dumb

if __name__ == '__main__':
    mat = csvToMatrix('tests/test_sheet_1.csv')
    inds, reasons, cols = all_dirty_cells(mat, header = 1, parallel = False, return_cols = True)
    for i in range(inds.shape[0]):
        true_inds = (inds[i, 0] + 1, inds[i, 1])
        print(f'Dirty cell found in cell {true_inds[1] + 1} of row \n{mat[true_inds[0]]}\n' +
              user_message(mat[true_inds], 
                           cols[true_inds[1]], 
                           reasons[i]) +
              f'\nSuggested: {clean_cell_dumb(mat[true_inds], cols[true_inds[1]], reasons[i])}\n')
