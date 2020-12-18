# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 15:06:59 2020

@author: HP
"""
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def title_build(titles):
    corpus=[]
    for title in titles:
        print(title)
        print('-'*40)
        title=re.sub('[^A-Za-z]',' ',title).lower()
        tokenized= word_tokenize(title)
        print(tokenized)
        print('-'*40)
        t1=[]
        for i in tokenized:
            t1.append(i)
        f_title=[word for word in tokenized if word not in stopwords.words('english')]
        print(f_title)
        f_title=' '.join(f_title)
        print('-'*40)
        corpus.append(f_title)
    return corpus

c=title_build(df['title'].values)

def description_build(desc):
    pass




























