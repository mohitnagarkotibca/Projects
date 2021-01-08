# -*- coding: utf-8 -*-
"""
Created on Sun Jun 28 11:51:52 2020

@author: HP
"""
import re 
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer

def title_build(titles):
    corpus = []        
    for i in range(0, len(titles)):         
      review = re.sub('[^a-zA-Z]',' ', titles[i])            
      review = review.lower()            
      review = review.split()            
      ps = PorterStemmer()            
      review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]            
      review = ' '.join(review)            
      corpus.append(review)
    return corpus

def description_build(desc):
    corpus1 = [] 
    for i in range(0, len(desc)):            
      review = re.sub('[^a-zA-Z]', ' ', desc[i])            
      review = review.lower()            
      review = review.split()            
      ps = PorterStemmer()            
      review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]            
      review = ' '.join(review)            
      corpus1.append(review)
    return corpus1



























