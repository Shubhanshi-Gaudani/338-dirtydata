from .Column import Column
from .utilities import can_be_float

def isCorrectDataType(cell_str, col):

    if col.column_type == 'alpha':
        typ = str
    else:
        if "." in cell_str:
            typ = float
        else:
            typ = int
    
    if not (isinstance(cell_str, typ)):
        incorrect_ind = col.index(cell_str)
        print('Datatype mismatch for element found at index ',incorrect_ind)
        return False
    
    return True
    

