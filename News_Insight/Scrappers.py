# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 22:52:43 2020

@author: HP
"""
import requests
import bs4
BeautifulSoup = bs4.BeautifulSoup

# from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import re
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
            if (('in' in link) and  ('pictures' in link)):
                continue
            links.append(link)
            titles.append(all_stories[i].find_all('a')[j].text)

                
            article = requests.get(link)
            article_content = article.content
            soup_article = BeautifulSoup(article_content, 'html.parser')
            content= soup_article.findAll('div',{'id':re.compile('content-body')})
            news.append(content[0].text)

    df= pd.DataFrame({'links':links,'title':titles,'news':news})
    return df

def scrap_theasianage():
    url='http://www.asianage.com/'
    r1= requests.get(url)
    coverpage = r1.content
    soup = BeautifulSoup(coverpage, 'html.parser')
    coverpage_news = soup.findAll('div',{'class':'single_left_coloum_wrapper other-top-stories'})
    titles=[]
    links=[]
    multiple_news=[]
    base='http://www.asianage.com'
    for d in coverpage_news[0].find_all('h3'):
        link= d.a['href']
        links.append(link)
        titles.append(d.text)
        r= requests.get(base+ link)
        article_content= r.content
        soup= BeautifulSoup(article_content,'html.parser')
        container= soup.find('div',{'id':'storyBody'})

        one_news=[]
        for info in container.find_all('p'):
            n= info.get_text()
            if n != '\xa0':
                one_news.append(n)
        multiple_news.append(' '.join(one_news))

    df= pd.DataFrame({'links':links,'title':titles,'news':multiple_news})
    return df

def scrap_theguardian():

    # url definition
    url = "https://www.theguardian.com/uk"

    # Request
    r1 = requests.get(url)
    r1.status_code

    # We'll save in coverpage the cover page content
    coverpage = r1.content

    soup1 = BeautifulSoup(coverpage, 'html.parser')

    # News identification
    coverpage_news = soup1.find_all('h3', class_='fc-item__title')

    number_of_articles =len(coverpage_news)

    # Empty lists for content, links and titles
    # Empty lists for content, links and titles
    news_contents = []
    list_links = []
    list_titles = []
    number_of_articles= len(coverpage_news)

    for n in np.arange(0, number_of_articles):

        # We need to ignore "live" pages since they are not articles
        if "live" in coverpage_news[n].find('a')['href']:  
            continue

        # Getting the link of the article
        link = coverpage_news[n].find('a')['href']
        list_links.append(link)

        # Getting the title
        title = coverpage_news[n].find('a').get_text()
        list_titles.append(title)

        # Reading the content (it is divided in paragraphs)
        article = requests.get(link)
        article_content = article.content
        soup_article = BeautifulSoup(article_content, 'html.parser')
        bodies = soup_article.find_all('div', class_='content__article-body from-content-api js-article__body')
        for body in bodies:
            x= body.find_all('p')
            list_paragraphs = []
            for p in np.arange(0, len(x)):
                paragraph = x[p].get_text()
                list_paragraphs.append(paragraph)
                final_article = " ".join(list_paragraphs)

        news_contents.append(final_article)
        
    df= pd.DataFrame({'links':list_links,'title':list_titles,'news':news_contents})
    index= df['news'].drop_duplicates().index
    df= df.loc[index]        
    return df


def scrap_themint():
    url='https://www.livemint.com/latest-news/'
    r1= requests.get(url)
    coverpage = r1.content
    soup = BeautifulSoup(coverpage, 'html.parser')
    cover = soup.find_all('div',{'id':'mylistView'})
    container = cover[0].find_all('div',{'class':'listingNew clearfix impression-candidate'})

    titles=[]
    links=[]
    news=[]
    for headline in container:
    #     print(headline.find('div',{'class':'headlineSec'}).find('h2').get_text().strip())
        link=  headline.find('div',{'class':'headlineSec'}).find('h2').a['href']
        base='https://www.livemint.com'
        url= base +link

        r= requests.get(url)
        article_content= r.content
        soup= BeautifulSoup(article_content,'html.parser')
        paragraph_list= soup.find('div',{'class':'paywall'})
        info=[]
        for para in paragraph_list.find_all('p')[:-2]:
            cont= para.get_text()
            print(cont)
            info.append(cont)

        titles.append(title)
        links.append(link)
        news.append(' '.join(info))
    df= pd.DataFrame({'links':links,'title':titles,'news':news})
    return df