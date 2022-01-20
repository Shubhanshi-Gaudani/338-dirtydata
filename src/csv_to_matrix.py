import pandas as pd

def csvToMatrix(csv_name):
    """Takes the name of the csv file and returns the 2D matrix version of the file.
    Args:
        csv_name (str) : the name of the csv file
    Returns:
        result_mat (2d array) : Matrix version of the csv file
    """
    df = pd.read_csv(csv_name)
    result_mat = df.to_numpy()
    return result_mat