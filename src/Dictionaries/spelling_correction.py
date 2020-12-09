# MIT License
# 
# Copyright (c) 2020 Sameer Merchant
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from distance_functions import levenshtein_distance, jaccard_distance


def partial_match(words, vocab):
    partial_matches = set()
    for w in vocab:
        for word in words:
            if word in w:
                partial_matches.add(w)

    return partial_matches


def known(words, vocab): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in vocab)


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = ' -abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def inserts_one(word, c):
    "Generate words with insert one edits"
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    inserts    = [L + c + R               for L, R in splits]
    return set(inserts)


def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


def scrammble(word):
    "Generate Scrambled words with two edits "
    words = set()
    
    for i in range(len(word)):
        letter = word[i]

        if i < len(word):
            w = "".join([word[:i] + word[i+1:]])
        else:
            w = "".join(word[:i])

        for word in inserts_one(w, letter):
            words.add(word)
            for e1 in edits2(word):
                words.add(e1)
    print(words)
    return words


def candidates(word, vocab): 
    "Generate possible spelling corrections for word."
    return set(known([word], vocab) or 
            known(edits1(word), vocab) or 
            known(edits2(word), vocab) or 
            #partial_match(edits1(word), vocab) or
            #partial_match(edits2(word), vocab) or
            #partial_match([word], vocab)
            [word])

def spelling_correction(word, vocab): 
    "Most probable spelling correction for word."
    normalized_word = word.lower()

    if normalized_word in vocab:
        return [ (vocab_dict.get(word, word), 0)]

    candidate_word = candidates(normalized_word, vocab)

    #suggested_words_list = [(w, jaccard_distance(normalized_word ,w)) for w in candidate_word]
    suggested_words_list = [(w, levenshtein_distance(normalized_word ,w)) for w in candidate_word]
    suggested_words_list.sort(key=lambda x: (x[1], x[0]))

    suggestions = [(vocab_dict.get(w, w), d) for w, d in suggested_words_list]
    return suggestions


if __name__ == '__main__':
    from pprint import pprint
    from test_vocab import *

    vocab_dict = {w.lower(): w for w in vocab}
    normalized_vocab = [w for w in vocab_dict.keys()]
    test_words = ['rmcast', 'evpmPfRxtx', 'evpnenabeld', 'evpnenabled', 'evpnenaled', 'evpnfxrx']


    for word in test_words:
        result = spelling_correction(word, normalized_vocab)
        print("Word:{} Suggestions: {}".format(word, result))
