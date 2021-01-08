# -*- coding: utf-8 -*-
"""
Created on Sat Jun 27 09:59:51 2020

@author: HP
"""


from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import pandas as pd


categories=['UFC','FOOD','TRAVEL','MOVIES','BATMAN','BIKE','CARS','INDIAN POLITICS','HEALTH CRISIS']
UFC= pd.DataFrame(columns=['title','link','description','category'])
FOOD= pd.DataFrame(columns=['title','link','description','category'])
TRAVEL= pd.DataFrame(columns=['title','link','description','category'])
MOVIES=pd.DataFrame(columns=['title','link','description','category'])
BATMAN=pd.DataFrame(columns=['title','link','description','category'])
BIKE=pd.DataFrame(columns=['title','link','description','category'])
CARS=pd.DataFrame(columns=['title','link','description','category'])
INDIAN_POLITICS=pd.DataFrame(columns=['title','link','description','category'])
HEALTH_CRISIS=pd.DataFrame(columns=['title','link','description','category'])

frames=[]

run=[]
for category in categories:    
    category=category.replace(' ','')
    url=f'https://www.youtube.com/results?search_query={category}'
    driver=webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    run.append('A')
    driver.execute_script('window.scrollTo(0,(window.pageYOffset+3040))')
    time.sleep(15)
    run.append('B')
    source=driver.page_source
    
    S= BeautifulSoup(source,'html.parser')
    container=S.find_all('a',{'id':'video-title'})
    run.append('C') 
    titles=[]
    for title in container:
        titles.append(title['title'])
    run.append('D')
    links=[]
    for link in container:
        links.append(link['href'])
    run.append('E')
    d_container= S.find_all('yt-formatted-string',{'id':'description-text'})
    descs=[]
    for desc in d_container:
        descs.append(desc.text)
    c= f'{category} '*len(titles)
    cat= c.split()
    run.append('|')
    
    for d in [UFC,FOOD,TRAVEL,MOVIES,BATMAN,BIKE,CARS,INDIAN_POLITICS,HEALTH_CRISIS]:
        d=pd.DataFrame({'title':titles,'link':links,'description':descs[:len(titles)],'category':cat})
        frames.append(d)

print(len(titles))
print(len(links))
print(len(descs))
print(len(cat))

df=pd.concat(frames,axis=0)

df.to_csv('Youtube.csv')






















