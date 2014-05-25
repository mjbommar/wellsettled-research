# -*- coding: utf-8 -*-
"""
The :mod:`wsr.process.parse` provides methods to parse English language
sentences into structural representations, e.g., sentence diagrams.

Author: Michael J Bommarito II <michael@bommaritollc.com>
Date: 2014-05-25
"""

# Standard imports
import os

# WSR imports
from wsr.config import BASE_PATH

# NLTK imports
import nltk.parse.stanford

# Setup some of the Stanford parser paths
os.environ['STANFORD_MODELS'] = os.path.join(BASE_PATH,
                                             'stanford-parser')
os.environ['STANFORD_PARSER'] = os.path.join(BASE_PATH,
                                             'stanford-parser')

STANFORD_GRAMMAR = os.path.join(BASE_PATH,
                                'stanford-parser',
                                'englishPCFG.ser.gz')

sentence_parser = nltk.parse.stanford.StanfordParser(model_path=\
                                                     STANFORD_GRAMMAR)
