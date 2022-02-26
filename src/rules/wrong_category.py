import numpy as np
import spacy
from .rule_base import RuleBaseClass
  
import en_core_web_sm
nlp = en_core_web_sm.load()

_COUNT_PER_100_LINES = 2
_NUM_CATS_PER_100 = 2

class WrongCategory (RuleBaseClass):
    """Checks if a cell is different from the most common categories."""
    def is_dirty(self, cell_str, col):
        counts = col.by_count[cell_str]
        cats = col.counts_over_thresh
        if col.length > 100:
            per_100 = lambda n: 100 * n / col.length 
            counts = per_100(counts)
            cats = per_100(cats)

        return counts <= _COUNT_PER_100_LINES and cats >= _NUM_CATS_PER_100

    def message(self, cell_str, col):
        return ('This row appears to have a small number of categories, but ' +
                f'{cell_str} is not one of them.')

    def clean(self, inds, sheet, col, all_dirty):
        dict = col.by_count
        word = sheet[tuple(inds)]
        cur_tok = nlp(str(word))
        max_sim = 0
        best_guess = word
        words = ""
        for i, (j,k) in enumerate(dict.items()):
            if k >=  _COUNT_PER_100_LINES + 1:
                words = words + " " + j
      
        tokens = nlp(words)

        for token in tokens:
            if cur_tok.similarity(token) > max_sim:
                max_sim = cur_tok.similarity(token)
                best_guess = token.text
        return best_guess
        # https://www.geeksforgeeks.org/python-word-similarity-using-spacy/
