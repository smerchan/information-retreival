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
from collections import defaultdict
from distance_functions import levenshtein_distance

class TermDictionary(object):
    """ 
    A dictionary of terms 
    The class maintain a dictionary of terms. 
    It provides utility to lookup terms that match closest to a word 

    Attributes:
    -----------
      vocab: Iterable List or Set of alphanumeric strings (terms)

    Methods
    -------
      add_term(word)
      search_terms(word)
    """
    def __init__(self, vocab):
        """
        Parameters
        ----------
          vocab: list or Set 
             A list or set of str (terms)
        """
        self.terms_dict = { w.lower(): w for w in vocab }
        self.trigram_dict = TermDictionary.build_trigram_term_dict(self.terms_dict.keys())
        return 

    @staticmethod
    def get_trigrams(term):
        trigram_list = list()
        augmented_term = '$' + term + '$'
        for i in range(len(augmented_term)-2):
            trigram_list.append(augmented_term[i:i+3])
        return trigram_list

    @staticmethod
    def build_trigram_term_dict(terms=None):
        trigram_dict = defaultdict(list)

        for term in terms:
            for trigram in TermDictionary.get_trigrams(term):
                trigram_dict[trigram].append(term)
        return trigram_dict


    def add_term(self, word):
        """
        Parameters
        ----------
          word: str
              Lookup word in the dictionary 
        """
        if type(word) == str:
            return 

        if not word:
            return 

        self.terns_dict[word.lower()] = word
        return


    def search_terms(self, word):
        """ 
        Parameters
        -----------
          word: str 
             Lookup this word in the terms dictionary 

        Returns
        -------
          list 
            A sorted list of tuples (term, distance). The 'distance' is edit distance 
            from search term. The tuples are sorted in ascending order based on edit 
            distance
        """
        norm_word = word.lower()

        if norm_word in self.terms_dict:
            return [ (self.terms_dict.get(norm_word), 0) ]

        suggested_terms = list()
        for trigram in TermDictionary.get_trigrams(norm_word):
            suggested_terms.extend(self.trigram_dict.get(trigram, []))

        suggested_terms = set(suggested_terms)
        candidate_words = [ (self.terms_dict.get(term), levenshtein_distance(term, norm_word)) 
                             for term in suggested_terms ]
        candidate_words.sort(key=lambda x: (x[1], x[0]))
        return candidate_words


if __name__ == '__main__':
    from test_vocab import *
    from pprint import pprint

    test_words = ['evpnRecev', 'evpnRecevd', 'evpRecd', 'evpnRecv', 'evpnRcv', 'evpnRx', 'evpn*Rx', 'intf', 'mac', 'addr', 'ipaddr']
    termDict = TermDictionary(vocab)

    for word in test_words:
        suggested_words = termDict.search_terms(word)
        print("Query Word: {}, Suggested: {}\n".format(word, suggested_words))

