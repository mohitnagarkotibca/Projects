# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 15:00:11 2020

@author: Lenovo
"""
#mae_goal = less 16646.68172
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from scipy import stats
import seaborn as sns

hptrain= pd.read_csv('data/train.csv')
hptest= pd.read_csv('data/test.csv')
hptrain.replace('nan',np.NaN,inplace=True)


percent_null=(hptrain.isna().sum()[hptrain.isna().sum()>0]/hptrain.shape[0])*100
percent_null_columns_high=list(percent_null[percent_null>50].index)

#missing value------------------------------------------------------------------------------------------------------
#since data bahut missing hai or fireplace quality, i dont think utna matter karega
percent_null_columns_high.append('FireplaceQu')
hptrain.drop(percent_null_columns_high,axis=1,inplace=True)
hptest.drop(percent_null_columns_high,axis=1,inplace=True)
percent_null=(hptrain.isna().sum()[hptrain.isna().sum()>0]/hptrain.shape[0])*100
percent_null_columns_less=list(percent_null[percent_null<6].index)
hptrain.drop(percent_null_columns_less,axis=1,inplace=True)
hptest.drop(percent_null_columns_less,axis=1,inplace=True)

hptrain['LotFrontage'].describe(percentiles=[0.2,0.3,0.7,0.8])


#removing null values in test data
z1=hptest.isna().sum()[hptest.isna().sum()>0]
test_col_missing_less=list(z1[z1<5].index)
hptest.dropna(subset=test_col_missing_less,inplace=True)

hptest['LotFrontage'].describe()
hptest['LotFrontage'].ffill(inplace=True)

#sns.boxplot(hptest['LotFrontage'])
#hptest['LotFrontage'].plot(kind='density')
#hptrain['LotFrontage'].plot(kind='density')
#plt.xlim(0,320)

#since the skew is to the right mean>median
#it is better to fill LotFrontage's nan value to median

hptrain['LotFrontage'].fillna(hptrain['LotFrontage'].median(),inplace=True)

#Outliers-------------------------------------------------------------------------------------------
numeric_data=hptrain.select_dtypes(exclude='object')
numeric_data.drop('Id',axis=1,inplace=True)
z=stats.zscore(numeric_data)
z_scoredf=pd.DataFrame()
li=numeric_data.columns

for i in range(numeric_data.shape[1]):
    z_scoredf[li[i]]=pd.Series(z[0:,i])

no_o_z_scoredf=z_scoredf[(z_scoredf<3.5).all(axis=1)]
no_o_z_scoredf=z_scoredf[(z_scoredf>-3.5).all(axis=1)]
good_index=no_o_z_scoredf.index
hptrain=hptrain.iloc[good_index]



#check cardinality

categorical_cols=hptrain.select_dtypes('object').columns
cardinality_col={}
for col in categorical_cols:
    cardinality_col[col]= hptrain[col].nunique()
    
low_cardinality_cols=list({k for k,v in cardinality_col.items() if v < 8})
high_cardinality_cols=list({k for k,v in cardinality_col.items() if v > 8})

hptrain=hptrain.drop(high_cardinality_cols,axis=1)
hptest= hptest.drop(high_cardinality_cols,axis=1)
X=hptrain.drop('SalePrice',axis=1)
y=hptrain['SalePrice'].copy()
train_x,val_x,test_y,val_y= train_test_split(X,y)
categorial_transformer= OneHotEncoder(handle_unknown='ignore',sparse=False)
preprocessor=ColumnTransformer(transformers=[('A',categorial_transformer,low_cardinality_cols)])


model=RandomForestRegressor(n_estimators=100)
My_pipeline= Pipeline(steps=[('preprocess',preprocessor),('model',model)])
My_pipeline.fit(train_x,test_y)
y_pred=My_pipeline.predict(val_x)
print( mean_absolute_error(val_y,y_pred))

