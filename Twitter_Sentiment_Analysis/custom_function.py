# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 08:28:36 2020

@author: HP
"""

import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
nlp= spacy.load('en_core_web_sm')
def symbols(tweet):
    tweet= re.sub(r'#[a-z]+\s+?','',tweet)
    print(tweet)
    tweet= re.sub(r'[^A-Za-z\s]','',tweet).strip()
    return tweet
#clean(nlp(symbols('she makes everything better. #chihuahua #puppy   #love ')))
        
def clean(doc):
    lemma_doc= [token.lemma_ for token in doc if token.pos_ not in['PRON','SPACE']]
    return [token for token in lemma_doc if nlp.vocab[token].is_stop!= True]
def hashtag_extract(text):
    text= ' '.join(re.findall(r'#[\w+]+',text)).replace('#','').split(' ')
    return text


