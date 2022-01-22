import re
 
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
 
def is_email(cell_str, col):
 
if col.column_type == 'alpha':
    if(re.fullmatch(regex, cell_str)):
        return True 
    
return False


#Code from : https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/