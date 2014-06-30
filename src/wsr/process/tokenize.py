# -*- coding: utf-8 -*-
"""
The :mod:`wsr.process.tokenize` provides methods to tokenize paragraphs,
sentences, and words.

Author: Michael J Bommarito II <michael@bommaritollc.com>
Date: 2014-05-24
"""

# NLTK imports
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktWordTokenizer, \
    PunktParameters

# Import stopword list
english_stopwords = stopwords.words('english')


# Customizer sentence tokenizer
punkt_param = PunktParameters()
punkt_param.abbrev_types = [x.lower().strip() for x in \
                                set(['id', 'al', 'mr', 'mrs',
                                         'prof', 'inc', 'llc', 'co',
                                         'llp', 'pp', 'f', 'app',
                                         '2d', '3d', 'ch', 's', 'us',
                                         'cert', 'rev', 'i', 'ii', 'iii',
                                         'a', 'b', 'c', 'd', 'e', 'f',
                                         'g', 'h', 'i', 'j', 'k', 'l',
                                         'm', 'n', 'o', 'p', 'q', 'r', 's',
                                         't', 'u', 'v', 'w', 'x', 'y', 'z',
                                         ')', 'no', 'cir', 'ca', 'c.a',
                                         'fed', 'sec', 
                                         'jan', 'feb', 'mar', 'apr', 'jun',
                                         'jul', 'aug', 'sep', 'oct', 'nov',
                                         'dec', 'ala', 'vt', 'st', 'u.s', 
                                         'viz', 'pet', 'stat', 'rev', 'l.d',
                                         's.c', 'appx', 'dept', 'cf', 'u.s.a',
                                         'dall', 'ins', 'etc', 'i.e', 'e.g',
                                         'inf', 'sup', 'ry', 'r.r', 'u.s.c.a',
                                     'a.l.r', 'b.t.a', 'u.s.c', 'c.f.r',
                                     'fed.r.civ.p', 'f.c.c', 'fed.r.crim.p',
                                     'i.n.s', 'u.s.s.g', 'u.a.w', 'fed.r.app.p',
                                     'j.p.m.l', 's.e.c', 'u.s.d.c', 'g.b.r',
                                     'f.d.i.c', 'f.e.r.c', 'f.r.e', 'n.l.r.b',
                                     'pub.l', 'i.l.m', 'u.n.t.s', 'u.s.s', 'tex',
                                     'd.c', 'r.g.w.r', 's.ct', 'cert', 'den', 'w.r',
                                     'ed', 'stat', 'c.c.a', 'supp'])]

# Build word and sentence tokenizer
sentence_tokenizer = PunktSentenceTokenizer(punkt_param)
word_tokenizer = PunktWordTokenizer()
