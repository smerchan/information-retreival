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
"""
Collection of distance functions 
"""
from pprint import pprint 

def jaccard_distance(w1, w2):
    """
    Parameters:
    -----------
      w1: str
      w2: str

    Returns:
    --------
      float: 
         Jaccard distance between w1 and w2 
    """
    ws1 = set(w1)
    ws2 = set(w2)

    if (len(ws1) > 1) or (len(ws2) > 1):
        dist = 1 - len(ws1.intersection(ws2))/len(ws1.union(ws2))
    else:
        dist = 0
    return dist


def common_characters(w1, w2):
    """
    Parameters:
    ----------
      w1: str
      w2: str

    Returns:
    --------
       int:
          Number of characters common between two strings
         
    """
    ws1 = set(w1)
    ws2 = set(w2)
    return len(ws1.intersection(ws2))
    

def levenshtein_distance(w1, w2):
    """
    Parameters:
    ----------
      w1: str
      w2: str

    Returns:
    --------
      int:
        Returns Levenshtein edit distance between the two strings 
    """
    n1 = len(w1) + 1
    n2 = len(w2) + 1
    dist = [[0]*n2 for _ in range(n1)]

    for i in range(n1):
        dist[i][0] = i

    for j in range(n2):
        dist[0][j] = j

    for x in range(1, n1):
        for y in range(1, n2):
            if w1[x-1] == w2[y-1]:
                dist[x][y] = min(dist[x-1][y-1], 
                                 dist[x-1][y] + 1, 
                                 dist[x][y-1] + 1)
            else:
                dist[x][y] = min(dist[x-1][y-1] + 1, 
                                 dist[x-1][y] + 1,
                                 dist[x][y-1] + 1)
    return dist[n1-1][n2-1]

if __name__ == '__main__':
    w1 = 'faster'
    w2 = 'fct'
    d = levenshtein_distance(w1, w2)
    print(d)
