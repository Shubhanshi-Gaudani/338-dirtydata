from unicodedata import numeric
import pandas as pd
import xlwings as xw
from .rules import NumOutlier, IsNA, IsIncorrectDataType, MissingData, WrongCategory
from .rules import HasTypo, EmailChecker
from .ui import CLEAN_XL_PATH



def highlight_excel():
    color_dict = {}
    #Define the colours that we want in the highlighted cells:
    #Light Salmon Pink 
    color_dict[MissingData] = (255, 154, 162)
    #Crayola's Periwinkle
    color_dict[IsNA] = (199, 206, 234)
    #Dirty White
    color_dict[NumOutlier] = (226, 240, 203)
    #Phillipine Silver 
    color_dict[HasTypo] = (177, 177, 177)
    #Columbia Blue 
    color_dict[IsIncorrectDataType] = (192, 228, 241)
    #Cookies and Cream
    color_dict[WrongCategory] = (232, 215, 173)
    #Tea Green
    color_dict[EmailChecker] = (208, 246, 210)

    file_name = CLEAN_XL_PATH
    wb = xw.Book(file_name)
    xl_sheet = wb.sheets['Sheet1']
    xl_sheet.range("A1:A10").color = Excellent
    xl_sheet.range("B1:B10").color = Better
    xl_sheet.range("C1:C10").color = Good
    xl_sheet.range("D1:D10").color = Average
    xl_sheet.range("E1:E10").color = Bad

highlight_excel()