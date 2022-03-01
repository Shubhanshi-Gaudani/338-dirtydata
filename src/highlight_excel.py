import pandas as pd
import xlwings as xw


def highlight_excel():

    #Define the colours that we want in the highlighted cells:
    
    Excellent = (0, 245, 57)
    Better = (93, 245, 128)
    Good = (238, 242, 0)
    Average = (255, 92, 92)
    Bad = (255, 0, 0)

    #
    file_name = 'test_sheets/temp.xlsx'
    wb = xw.Book(file_name)
    xl_sheet = wb.sheets['Sheet1']
    xl_sheet.range("A1:A10").color = Excellent
    xl_sheet.range("B1:B10").color = Better
    xl_sheet.range("C1:C10").color = Good
    xl_sheet.range("D1:D10").color = Average
    xl_sheet.range("E1:E10").color = Bad

highlight_excel()