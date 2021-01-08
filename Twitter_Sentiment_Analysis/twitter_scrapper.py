# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 14:45:03 2020

@author: HP

"""
from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

begin_date= dt.date(2020,7,2)
end_date= dt.date(2020,7,3)
limit=10
lang= 'english'
#user= 'narendra modi'
tweets= query_tweets("PM Modi", begindate= begin_date, enddate=end_date,limit=limit,lang=lang)
df= pd.DataFrame(t.__dict__ for t in tweets)[['screen_name','text']]




