# -*- coding: utf-8 -*-
"""
Created on Tue May  5 19:54:38 2020

@author: HP
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

train=pd.read_csv('data/train.csv')

test=pd.read_csv('data/test.csv')


def calculate_na(train,test):
    train_na=train.isna().sum()[train.isna().sum()>0]/train.shape[0]*100
    test_na=test.isna().sum()[test.isna().sum()>0]/test.shape[0]*100
    df=pd.DataFrame({'train':train_na,'test':test_na}).replace(np.nan,0).sort_values(by='train',ascending=False)
    return train_na,test_na,df


train_na,test_na,df=calculate_na(train,test)

high_na=train_na[train_na>40]

train[high_na.index]=train[high_na.index].fillna('missing')
test[high_na.index] =test[high_na.index].fillna('missing')

train_na,test_na,df=calculate_na(train,test)




#---------------------------------------
#def drop_col(cols,train=None,test=None):
#    train=train.drop(cols,axis=1)
#    test= test.drop(cols,axis=1)
#    return train,test
#train,test=drop_col(high_na,train,test)
#train_na,test_na,df=calculate_na(train,test)
#train=train.dropna()
#test=test.dropna()
#a,b,c=calculate_na(train,test)

train['LotFrontage'].describe()
train['LotFrontage'].plot(kind='box')
sns.distplot(train['LotFrontage'].dropna())

#decided to limit lotfrontage to 150
train=train.query('LotFrontage < 150')

#decided to fill test lotfrontage to mean, because it is a testing data, more variation more good 

test['LotFrontage']=test['LotFrontage'].fillna(train['LotFrontage'].mean())

a,b,c=calculate_na(train,test)

train_na=c[c['train']>0].index
test_na =c[c['test']>0].index 
   
from sklearn.impute import SimpleImputer
si= SimpleImputer(strategy='most_frequent')

imputed_train=pd.DataFrame(si.fit_transform(train[train_na]),index=train[train_na].index)

imputed_train.columns= train_na

train=train.drop(train_na,axis=1)

train=pd.concat([train,imputed_train],axis=1)

a,b,c=calculate_na(train,test)

set(train.columns)- set(test.columns)

for col in test_na:
    if test[col].dtypes=='object':
        test[col]= test[col].fillna(max(train[col].values))
    else:
        test[col]= test[col].fillna(train[col].median())

a,b,c=calculate_na(train,test)

#-----------------------------------------

#outliers
train=train.query('SalePrice < 300000')

#categorical values
object_col= train.select_dtypes('object').columns

def  calculate_uni(col):
    a1= train[col].nunique()
    a2= test[col].nunique()
    return pd.DataFrame({'train':a1,'test':a2}).sort_values(by='train',ascending=False)


high=calculate_uni(object_col).index

good_col=[col for col in high if set(train[col]) == set(test[col])]

bad_cols= set(high)- set(good_col)
train= train.drop(bad_cols,axis=1)
test= test.drop(bad_cols,axis=1)

calculate_uni(good_col)

from sklearn.preprocessing import LabelEncoder
le=LabelEncoder()


for col in good_col:
    train[col]=le.fit_transform(train[col])
    test[col]= le.transform(test[col])



from sklearn.ensemble import RandomForestRegressor

model=RandomForestRegressor()

from sklearn.model_selection import train_test_split
x=train.drop('SalePrice',axis=1)
y=train['SalePrice']

train_x,test_x,train_y,test_y=train_test_split(x,y)    
  
model.fit(train_x,train_y)

y_predict= model.predict(test_x)

from sklearn.metrics import mean_absolute_error
mae_score=mean_absolute_error(y_predict,test_y)


###1 : 14054.209834929436
##RFG: 16465k
#test.isna().sum()
#

output=model.predict(test)


output2= pd.DataFrame({'Id':test['Id'],'SalePrice':output})
output2=output2.astype('int32')
output2.to_csv('House_pricing1.6.1.csv',index=False)