from word_stats import word_count, mean, std_deviation
from copy import copy

chars = 'abcdefghijkplnopqrstuvwxyz'
chars += chars.upper()

two_sigma = mean() + std_deviation() * 2

def edits(word, max_dist=2):
    word = list(word)
    if max_dist > 0:
        for i in range(len(word)):
            for char in chars:
                new_word = copy(word)
                new_word[i] = char
                yield ''.join(new_word)
                for res in edits(new_word, max_dist-1):
                    yield res

def pick_max_count(word):
    _max = 0
    res = word
    for edit in edits(word):
        count = word_count(edit)
        if count > two_sigma:
            return edit
        if count > _max:
            _max = count
            res = edit
    return res
