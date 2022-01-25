import pandas as pd
import numpy as np

def csvToMatrix(csv_name):
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
            mat.append(line.split(','))
            assert len(mat[-1]) == len(mat[0]), len(mat) - 1
    return np.array(mat, dtype = str)
