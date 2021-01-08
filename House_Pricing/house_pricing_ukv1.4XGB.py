# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:00:11 2020

@author: Lenovo
"""
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
mae_dic={}


a_hptrain= pd.read_csv('data/train.csv')
a_hptest=pd.read_csv('data/test.csv')

high_na_cols=pd.DataFrame()

high_na_cols['Train']=(a_hptrain.isna().sum()[a_hptrain.isna().sum()>40]/a_hptrain.shape[0])*100
high_na_cols['Test']=(a_hptest.isna().sum()[a_hptest.isna().sum()>40]/a_hptest.shape[0])*100


a_drop_train_col=list(high_na_cols['Train'][high_na_cols['Train']>40].index)
a_drop_test_col=list(high_na_cols['Test'][high_na_cols['Test']>40].index)


b_hptrain= a_hptrain.drop(a_drop_train_col,axis=1)
b_hptest = a_hptest.drop(a_drop_train_col,axis=1)

        

for col in b_hptrain.columns:
    b_hptrain[col].ffill(inplace=True)
for col in b_hptest.columns:
    b_hptest[col].ffill(inplace=True)

b_catagorical_cols=list(b_hptrain.select_dtypes('object').columns)
    
b_good_categorical_col=[]
b_bad_categorical_col=[]

for col in b_catagorical_cols:
    if b_hptrain[col].nunique() == b_hptest[col].nunique():
        b_good_categorical_col.append(col)
    else:
        b_bad_categorical_col.append(col)


unique_val_cols=b_hptrain[b_good_categorical_col].nunique()[b_hptrain[b_good_categorical_col].nunique()<10]

c_hptrain= b_hptrain.drop(b_good_categorical_col,axis=1)
d_hptrain= c_hptrain.drop(b_bad_categorical_col,axis=1)

c_hptest= b_hptest.drop(b_good_categorical_col,axis=1)
d_hptest= c_hptest.drop(b_bad_categorical_col,axis=1)


d_hptrain=d_hptrain.astype('int32')
d_hptest= d_hptest.astype('int32')

preprocessor=ColumnTransformer(transformers=[("preprocess",OneHotEncoder(handle_unknown='ignore',dtype=np.int32),unique_val_cols)])

X=d_hptrain.drop('SalePrice',axis=1)
y=d_hptrain['SalePrice']


train_x,val_x,test_y,val_y = train_test_split(X,y)

from xgboost import XGBRegressor
model=XGBRegressor(n_estimators=5000,early_stopping_round=5, eval_set=[val_x,val_y],learning_rate=0.1,n_jobs=4)
model.fit(train_x,test_y)
y_pred=model.predict(d_hptest)

#mm=pd.DataFrame({'n_est':np.arange(50,150,11),'mean':scores})
##83---> 28562
##print(get_score(83))
##mae_dic['2nd attempt pipeline']=mean_absolute_error(Y_mae,val_y)


output= pd.DataFrame({'Id':d_hptest['Id'],'SalePrice':y_pred})
output=output.astype('int32')
output.to_csv('HPXGBoostSubmission.csv',index=False)
##1st attempt: 18k
##2nd attempt with pipeline: 28k
##3rd attempt with xggboost: 16.5k