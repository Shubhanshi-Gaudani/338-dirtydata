import numpy as np

def can_be_float(s):
    """Returns whether s can be cast as a float without exception.
    
    Args:
        s (str) : a string to check
        
    Returns:
        is_float (bool) : whether the string can be cast as a float
    """
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_float_char(c):
    """Returns whether the given character could be in a valid float string
    
    Args:
        c (str) : a single character
    
    Returns:
        could_be (bool) : whether the character could be in a valid float
    """
    return c.isnumeric() or c == '.' or c == '-'

def can_be_int(s):
    """Returns whether s can be cast as a int without exception.
    
    Args:
        s (str) : a string to check
        
    Returns:
        is_int (bool) : whether the string can be cast as a int
    """
    try:
        int(s)
        return True
    except ValueError:
        return False

def float_is_int(f):
    """Returns whether f is a close enough to the nearest integer.
    
    Args:
        f (float) : the float to look at 

    Returns:
        is_int (bool) : whether the float is basically an integer
    """
    return np.isclose(f, round(f))
