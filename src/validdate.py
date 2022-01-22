from datetime import datetime

def isDateValid(date, pattern = "%d/%m/%y"):
    try:
        datetime.strptime(date, pattern)
        return True
    except ValueError:
        return False
with open("filename.csv") as f:
    # split file into lines
    lines = f.readlines()
    lines = [x.replace("\n", "") for x in lines]
    header = lines[0]
    rows = lines[1:]
    for rowNumber, row in enumerate(rows, 1):
        columns = line.split(",")
        gotValidDate = False
        for column in columns:
            if isDateValid(column):
                gotValidDate = True
        if gotValidDate:
            print(f"Row {rowNumber} got at least one valid date")
