import numpy as np
from spellchecker import SpellChecker

def _typo_word(s):
    """Returns whether s is likely to be a typo."""
    return _clean_word(s) != s

def _clean_word(s):
    """Returns the most likely word the user meant based on s."""
    # return str(TextBlob(s.lower()).correct())
    spell = SpellChecker()
    return spell.correction(s)

def has_typo(cell_str, col):
    """Returns whether the string has a typo in it.
    
    Args:
        cell_str (str) : the raw text of that cell
        column (Column) : container for generic info about the column of that cell

    Returns:
        has_typo (bool) : whether or not the string has a typo in it
    """
    words = cell_str.split(' ')
    return any(map(_typo_word, words))

def typo_message(cell_str, col):
    """Returns a user-friendly message for why the cell is dirty.
    
    Args:
        cell_str (str) : the string version of the cell
        col (Column) : a container class with information about the column

    Returns:
        message (str) : a readable reason why the string was dirty
    """
    words = cell_str.split(' ')
    for word in words:
        if _typo_word(word):
            return f'{word} appears to be a typo. Did you mean {clean_typo(word)}?'
    raise ValueError(f'No typo present in {cell_str}.')

def clean_typo(cell_str):
    """Returns the desired imputed value based on cell_str.

    Note that this has a different signature than the other clean functions.
    
    Args:
        cell_str (str) : the string to be corrected.

    Returns:
        prediction (str) : what the model predicts should go in that cell
    """
    words = cell_str.split(' ')
    for i in range(len(words)):
        if _typo_word(words[i]):
            words[i] = _clean_word(words[i])
    return ' '.join(words)

