# -*- coding: utf-8 -*-

import re 
import nltk 
import pandas as pd
from nltk.corpus import stopwords 
from nltk.stem.porter import PorterStemmer
df=pd.read_csv('youtube.csv')
df_link = pd.DataFrame(columns = ["link"])        
df_title = pd.DataFrame(columns = ["title"])        
df_description = pd.DataFrame(columns = ["description"])        
df_category = pd.DataFrame(columns = ["category"])        
df_link = df['link'] 
df_title= df['title'] 
df_description = df['description'] 
df_category = df['category']

len(df.index)

corpus = []        
for i in range(0, 2672):
    review = re.sub('[^a-zA-Z]', ' ', df_title[i])            
    review = review.lower()            
    review = review.split()            
    ps = PorterStemmer()            
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]            
    review = ' '.join(review)            
    corpus.append(review)

corpus1 = [] 
for i in range(0, 2672):            
    review = re.sub('[^a-zA-Z]',' ',str(df_description[i]))            
    review = review.lower()            
    review = review.split()            
    ps = PorterStemmer()            
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]            
    review = ' '.join(review)            
    corpus1.append(review)

dftitle = pd.DataFrame({'title':corpus})
dfdescription = pd.DataFrame({'description':corpus1})

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
le=LabelEncoder()
dfcategory1 =pd.Series(le.fit_transform(df_category))
    

df_new = pd.concat([df_link, dftitle, dfdescription, dfcategory1], axis=1)


from sklearn.feature_extraction.text import CountVectorizer   
cv = CountVectorizer(max_features = 1500) 
X = cv.fit_transform(corpus, corpus1).toarray() 
y = df_new.iloc[:-1, 3].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

# from sklearn.ensemble import RandomForestClassifier
# classifier = RandomForestClassifier(n_estimators = 1000, criterion = 'entropy')
# classifier.fit(X_train, y_train)

# y_pred = classifier.predict(X_test)
# classifier.score(X_test, y_test)

# print(classification_report(y_test, y_pred))

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import *
# from sklearn.preprocessing import MinMaxScaler
# from sklearn import linear_model
# from sklearn.metrics import *
# print(classification_report(y_test, y_pred))

# from sklearn.svm import SVC
# classifier1 = SVC(kernel = 'linear', random_state = 0)
# classifier1.fit(X_train, y_train)

# y_pred1 = classifier1.predict(X_test)
# classifier1.score(X_test, y_test)

# from xgboost import XGBClassifier
# classifier3 = XGBClassifier()
# classifier3.fit(X_train, y_train)

# y_pred3 = classifier3.predict(X_test)
# classifier3.score(X_test, y_test)

