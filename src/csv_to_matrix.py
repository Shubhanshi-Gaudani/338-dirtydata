import pandas as pd
import numpy as np
from .utilities import can_be_float

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
                    row[-1] += cells[cell]
                else:
                    row.append(cells[cell])
            mat.append(row)
            if len(mat[-1]) < len(mat[0]):
                for _ in range(len(mat[0]) - len(mat[-1])):
                    mat[-1].append('')
            elif len(mat[-1]) > len(mat[0]):
                mat[-1] = mat[-1][:len(mat[0])]
    return np.array(mat, dtype = 'U128')

def has_header(mat):
    """Determines whether the spreadsheet has a header.
    
    Args:
        mat (np.array) : a 2D array of strings

    Returns:
        header (int) : how many rows to skip initially
    """
    all_strs = lambda i: not any(map(can_be_float, mat[i]))
    return int(all_strs(0) and 
               not all(map(all_strs, range(1, mat.shape[0]))))
