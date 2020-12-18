import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import numpy as np
import pandas as pd
import time
import re
def abc():
	print('hellp')
	
def scrap_the_hindu():
    url= 'https://www.thehindu.com/'

    r1= requests.get(url)

    r1.status_code

    coverpage= r1.content

    soup= BeautifulSoup(coverpage,'html.parser')


    all_stories = soup.find_all('div',{'class':"justIn-story"})
    length= len(all_stories)
    # length

    # all_stories[0].find('li').h3.a['href']
    # all_stories[0].find('li').a.text

    # for i in range(len(all_stories)):
    #     for j in range(len(all_stories[i])):
    #         print(all_stories[i].find_all('a')[j]['href'])


    links=[]
    titles=[]
    news=[]
    for i in range(len(all_stories)):
        for j in range(len(all_stories[i])):
            link= all_stories[i].find_all('a')[j]['href']
            links.append(link)
            titles.append(all_stories[i].find_all('a')[j].text)

            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html.parser')
            body = soup_article.find_all('div', class_='paywall')
            content = body[0].find_all('p')

            paragraph=[]
            for x in range(0,len(content)):
                para= content[x].get_text()
                paragraph.append(para)
            news.append(' '.join(paragraph))

    df= pd.DataFrame({'links':links,'title':titles,'news':news})
	df['title']= df['title'].str.replace(r'[0-9]{1,2}(mins|hrs)','')
    return df
	
