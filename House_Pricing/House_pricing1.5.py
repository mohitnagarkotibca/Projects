# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:10:37 2020

@author: HP
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

train= pd.read_csv('data/train.csv')
test= pd.read_csv('data/test.csv')
plt.subplots(figsize=(12,9))
sns.heatmap(train.corr(),square=True)
col=train.corr().nlargest(10,'SalePrice').index

sns.heatmap(train[col].corr(),annot=True)
features=train.columns.drop(['GarageCars','1stFlrSF'])
#plan to remove OverallQuality too

a_train= train[features]
a_test= test[features.drop('SalePrice')]

na_vals=(a_train.isna().sum()[a_train.isna().sum()>0]/a_train.shape[0]*100).sort_values()

col_remove= na_vals[na_vals>40].index

a_train.drop(col_remove,axis=1,inplace=True)
a_test.drop(col_remove,axis=1,inplace=True)

na_vals=(a_train.isna().sum()[a_train.isna().sum()>0]/a_train.shape[0]*100).sort_values()
d= na_vals[na_vals<5].index

a_train=a_train.dropna(subset=d)
a_test= a_test.dropna(subset=d)

r=(a_train.isna().sum()[a_train.isna().sum()>0]/a_train.shape[0]*100).sort_values().index

a_train['LotFrontage']=a_train['LotFrontage'].fillna(method='ffill')
a_test['LotFrontage']= a_test['LotFrontage'].fillna(method='ffill')

r=(a_train.isna().sum()[a_train.isna().sum()>0]/a_train.shape[0]*100).sort_values().index
b_train=a_train.dropna(subset=r)
b_test= a_test.dropna(subset=r)
b_test= b_test.dropna()


(b_train.isna().sum()[b_train.isna().sum()>0]/b_train.shape[0]*100).sort_values()


#
#
#(b_train.isna().sum()[b_train.isna().sum()>0]/b_train.shape[0]*100).sort_values()
#(b_test.isna().sum()[b_test.isna().sum()>0]/b_test.shape[0]*100).sort_values()
#
#

#outliers

b_train['SalePrice'].describe()
b_train=b_train.query('SalePrice < 250000')
b_train['SalePrice'].plot(kind='box')

#categorical variables

objects= b_train.select_dtypes('object')
objects_col=list(objects.columns)

def calculate_unique(train,test):
    a1= train.select_dtypes('object').nunique()
    a2= test.select_dtypes('object').nunique()
    return pd.DataFrame({'train':a1,'test':a2}).sort_values(by='train',ascending=False).replace(np.nan,0)

unique_val= calculate_unique(b_train,b_test)
plt.subplots(figsize=(12,8))
sns.boxplot(x=b_train['Neighborhood'],y=b_train['SalePrice'],orient=20)
a=plt.xticks(rotation=40)


good_cat=[]
bad_cat=[]
for col in unique_val.index:
    if unique_val['train'][col] == unique_val['test'][col]:
        good_cat.append(col)
    else:
        bad_cat.append(col)

b_train=b_train.drop(bad_cat,axis=1)
b_test= b_test.drop(bad_cat,axis=1)

unique_val=calculate_unique(b_train,b_test)

high_unique= unique_val[(unique_val['train'] > 10 )& (unique_val['test'] > 10)].index
b_train=b_train.drop(high_unique,axis=1)
b_test=b_test.drop(high_unique,axis=1)
calculate_unique(b_train,b_test)
unique_val=calculate_unique(b_train,b_test)

LE_cols= list(unique_val[unique_val>4].index)
OH_cols= list(unique_val[unique_val<5].index)
    
all_cols=list(LE_cols + OH_cols)

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

b_train['SaleType'].value_counts()

b_train.info()

le=LabelEncoder()
for col in LE_cols:    
    b_train[col+'enc']=le.fit_transform(b_train[col])
    
for col in LE_cols:
    b_test[col+'enc']= le.fit_transform(b_test[col])

b_train=b_train.drop(LE_cols,axis=1)

oh=OneHotEncoder(handle_unknown='ignore')
for col in OH_cols:
    b_train[col+'enc']=le.fit_transform(b_train[col])
    b_test[col+'enc']=le.fit_transform(b_test[col])

#
#b_train=b_train.drop(all_cols,axis=1)
#b_test=b_test.drop(all_cols,axis=1)
#
#calculate_unique(b_train,b_test)
#
#


