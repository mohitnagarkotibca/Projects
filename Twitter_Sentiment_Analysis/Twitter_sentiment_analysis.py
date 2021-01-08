# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 14:26:36 2020

@author: HP
"""

import pandas as pd
data_train= pd.read_csv('data/train.csv')
data_test= pd.read_csv('data/test.csv')

train=data_train.copy()
test=data_test.copy()


import spacy
nlp= spacy.load('en_core_web_sm')

from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer
import custom_function as cf

def data_cleaner(tweet):
    r_tweet =cf.symbols(tweet)
    doc=nlp(r_tweet)
    tweet= cf.clean(doc)
    return ' '.join(tweet)


#new_df= train.copy()
#new_df['clean_data']= [data_cleaner(tweet) for tweet in train['tweet']]
#new_df.to_pickle('train.pickle')

#test_df=[data_cleaner(tweet) for tweet in test['tweet']]

#pd.Series(test_df).to_pickle('test.pickle')

test_df= pd.read_pickle('test.pickle')
train_df=pd.read_pickle('train.pickle')
train_df=train_df.drop('id',axis=1)

import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

#mask=np.array('batman.jpg')
#some explorations--what are the most common words that people use in their positive tweets?
positivity=[re.sub(r'(user)?(amp)?','',word) for word in train_df.groupby('label').get_group(0)['clean_data']]
positive_words= pd.Series(' '.join(positivity).split(' '))
positive_words.value_counts()
wordcloud= WordCloud().generate(' '.join(positivity))
plt.imshow(wordcloud)
print('-'*40)
#what are the most common words that people use in their negative tweets?
negativity=[re.sub(r'(user)?(amp)?','',word) for word in train_df.groupby('label').get_group(1)['clean_data']]
negative_words= pd.Series(' '.join(negativity).split(' '))
negative_words.value_counts()
wordcloud2= WordCloud().generate(' '.join(negativity))
plt.imshow(wordcloud2)

#what are the most popular positive hashtags user add in their tweets?
hash_tags= [cf.hashtag_extract(text) for text in train['tweet']]
train_df['hash_tag']=hash_tags
pos_tags=[]
pos_tag=[[pos_tags.append(tag) for tag in li if tag.isalnum() ] for li in train_df.groupby('label').get_group(0)['hash_tag']]
tag_series=pd.Series(pos_tags)


import seaborn as sns
#plotting a bar plot
plt.figure(figsize=(15,12))
sns.barplot(y=tag_series.value_counts()[:50].index,x=tag_series.value_counts()[:50].values)

train_df['hash_tag']=hash_tags
neg_tags2=[]
neg_tag=[[neg_tags2.append(tag) for tag in li if tag.isalnum() ] for li in train_df.groupby('label').get_group(1)['hash_tag']]
tag_series=pd.Series(neg_tags2)
plt.figure(figsize=(15,12))
sns.barplot(y= tag_series.value_counts()[:50].index,x= tag_series.value_counts()[:50].values)


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split

cv= CountVectorizer(stop_words='english')
TRAINING_SET= pd.DataFrame(cv.fit_transform(train_df['clean_data']).todense())
    

x= TRAINING_SET
y= train['label']
train_x,val_x,test_y,val_y= train_test_split(x,y)

# %% [code]
train_x.head()

# %% [code]
from sklearn.linear_model import LogisticRegression
lr= LogisticRegression(max_iter=300)
lr.fit(train_x,test_y)

# %% [code]
y_pred= lr.predict(val_x)
from sklearn.metrics import mean_absolute_error

# %% [code]
mean_absolute_error(val_y,y_pred)

# %% [code]
testing=pd.DataFrame(cv.transform(test_df).todense())

# %% [code]
answer=pd.Series(lr.predict(testing))

# %% [code]
answer

# %% [code]
sollution= pd.DataFrame({'tweet':test_df,'Sentiment':answer})

# %% [code]
sollution.head()









