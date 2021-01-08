# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 04:51:49 2020

@author: Lenovo
"""
import pandas as pd
df1 = pd.DataFrame([['Kitchen Utensils',25,10,'Boston'], ['Gardening',35,15,'NYC']], columns=['Product', 'Sales in millions', 'Profit', 'Store_location'], index=[1,2])
df2 = pd.DataFrame([['Kitchen Utensils',35,7,'Somerville'], ['Switches',35,10,'Bridgewater'], ['Monitors',70,8,'Trenton']], columns=['Product', 'Sales in millions', 'Loss', 'Store_location'], index=[2,3,4])