import pandas as pd
import numpy as np

def duplicate_row(data):
    """Takes a whole dataset, returns which rows if any are duplicates.

    Args:
        data (pd) : a panda datafrae

    Returns:
        dup_rows (pd) : dataframe of duplicate rows
    """

    dup_rows = data[data.duplicated()]

    return dup_rows
