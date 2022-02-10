from ..utilities import can_be_float, can_be_int
from .missing_data import MissingData
from .num_outliers import NumOutlier
from .rule_base import RuleBaseClass

class IsIncorrectDataType (RuleBaseClass):
    """Checks if cells are the wrong datatype"""
    def is_dirty(self, cell_str, col):
        if can_be_int(cell_str):
            return col.column_type != 'int' and col.column_type != 'float'
        if can_be_float(cell_str):
            return col.column_type != 'float'
        return col.column_type != 'alpha'

    def message(self, cell_str, col):
        interp_type = 'alphabetical'
        if can_be_int(cell_str):
            interp_type = 'an integer'
        elif can_be_float(cell_str):
            interp_type = 'a decimal number'
        true_type = 'alphabetical words'
        if col.column_type == 'int':
            true_type = 'integers'
        elif col.column_type == 'float':
            true_type = 'decimal numbers'
        return (f'The cell {cell_str} was interpreted as {interp_type}, in contrast ' +
                f"to the column's most common datatype, {true_type}.")

    def clean(self, col):
        if col.column_type == 'alpha':
            return MissingData().clean(col)
        i = NumOutlier().clean(col)
        if col.column_type == 'int':
            return str(int(float(i))) # this is so dumb
        return i
