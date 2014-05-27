# -*- coding: utf-8 -*-
"""
The :mod:`wsr.process.stem` provides methods to stem English language
tokens.

Author: Michael J Bommarito II <michael@bommaritollc.com>
Date: 2014-05-26
"""

# NLTK imports
import nltk.stem
import string

# WSR imports
from wsr.process.tokenize import word_tokenizer, english_stopwords


stemmer = nltk.stem.PorterStemmer()


def process_sentence(sentence):
    """Process a sentence by tokenizing, removing stopwords, and stemming.
    """
    # Tokenize and remove stopwords
    tokens = [word.strip(string.whitespace).strip(string.punctuation) \
                      for word in word_tokenizer.tokenize(sentence)]
    nsw_tokens = [token for token in tokens if token \
                            not in english_stopwords]
    
    # Stem 
    stems = [stemmer.stem(token).lower() for token in nsw_tokens]
    
    return stems