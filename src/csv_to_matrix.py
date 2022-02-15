import pandas as pd
import numpy as np

def csvToMatrix(csv_name, delimiter = ','):
    """Takes the name of the csv file and returns the 2D matrix version of the file.
    Args:
        csv_name (str) : the name of the csv file
    Returns:
        result_mat (2d array) : Matrix version of the csv file
    """
    # df = pd.read_csv(csv_name, dtype = str)
    # result_mat = df.to_numpy(dtype = str)
    # return result_mat
    # unfortunately pandas does not handle empty cells well
    mat = []
    with open(csv_name, 'r') as sheet:
        for line in sheet:
            row = []
            cells = line.replace('\n', '').split(delimiter)
            row.append(cells[0])
            for cell in range(1, len(cells)):
                if (len(cells[cell]) and
                    len(cells[cell - 1]) and
                    cells[cell][-1] == '"' and 
                    cells[cell - 1][0] == '"'):
                    row[cell - 1] += cells[cell]
                else:
                    row.append(cells[cell])
            mat.append(row)
            if len(mat[-1]) != len(mat[0]):
                raise ValueError(f'row {len(mat)} of the spreadsheet has ' +
                                 f'length {len(mat[-1])} instead of the correct ' +
                                 f'length {len(mat[0])}.')
    return np.array(mat, dtype = 'U128')
