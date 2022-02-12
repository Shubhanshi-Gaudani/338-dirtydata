import numpy as np
from spellchecker import SpellChecker
from .rule_base import RuleBaseClass

class HasTypo (RuleBaseClass):
    """Checks if a cell has a typo in it."""
    def __init__(self):
        self.checker = SpellChecker()

    def _typo_word(self, s):
        """Returns whether s is likely to be a typo."""
        return self._clean_word(s) != s

    def _clean_word(self, s):
        """Returns the most likely word the user meant based on s."""
        return self.checker.correction(s)

    def is_dirty(self, cell_str, col):
        words = cell_str.split(' ')
        return any(map(self._typo_word, words))

    def message(self, cell_str, col):
        words = cell_str.split(' ')
        for word in words:
            if self._typo_word(word):
                return f'{word} appears to be a typo. Did you mean {self._clean_word(word)}?'
        raise ValueError(f'No typo present in {cell_str}.')

    def clean(self, inds, sheet, col):
        words = sheet[tuple(inds)].split(' ')
        for i in range(len(words)):
            if self._typo_word(words[i]):
                words[i] = self._clean_word(words[i])
        return ' '.join(words)
