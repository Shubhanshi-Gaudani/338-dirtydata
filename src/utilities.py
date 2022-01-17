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