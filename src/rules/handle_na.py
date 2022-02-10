from .rule_base import RuleBaseClass

class IsNA (RuleBaseClass):
    """Checks is cells are 'na'."""
    def is_dirty(self, cell_str, col):
        missing_values = {"n/a", "na", "--", "-","nan","NaN", "not applicable"}
        if cell_str.lower() in missing_values and cell_str != 'NA': 
            return True
        else:
            return False

    def message(self, cell_str, col):
        return (f'This cell "{cell_str}" was interpreted as a variation of "NA". ' +
            'We suggest standardizing all such cells to "NA".')

    def clean(self, col):
        return 'NA'
