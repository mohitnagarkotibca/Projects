# -*- coding: utf-8 -*-
import pandas as pd 
import nltk
import text_preprocessing2 as tp
from sklearn.preprocessing import LabelEncoder

df=pd.read_csv('youtube.csv').drop('Unnamed: 0',axis=1)
df.isna().sum()
df=df.dropna(how='any')
le= LabelEncoder()
categories=pd.Series(le.fit_transform(df['category']))


title = tp.title_build(df['title'].values)
print(title)
desc  = tp.description_build(df['description'].values)
print(desc)
dftitle = pd.DataFrame({'title':title})
dfdescription = pd.DataFrame({'description':desc})
df_new = pd.concat([df['link'], dftitle, dfdescription, categories], axis=1)

from sklearn.feature_extraction.text import CountVectorizer   
cv = CountVectorizer(max_features = 1500) 
X = cv.fit_transform(title, desc).toarray() 
y = df_new.iloc[:, 3].values
    































