from datetime import datetime

def isDateValid(date, pattern = "%d/%m/%y"):
    try:
        datetime.strptime(date, pattern)
        return False
    except ValueError:
        return True
