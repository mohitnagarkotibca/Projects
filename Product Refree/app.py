import pandas as pd
import numpy as np


from selenium import webdriver
from selenium.webdriver.edge.options import Options
# from selenium.webdriver import Edge
from msedge.selenium_tools import EdgeOptions,Edge

from selenium.common.exceptions import NoSuchElementException
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from IPython.display import Image
import datetime
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import math
from time import sleep
from tqdm import tqdm
import os
from IPython.display import clear_output
options = EdgeOptions()
options.use_chromium = True
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
driver = Edge(executable_path=f'{os.getcwd()}/driver/msedgedriver.exe',options = options)

# give me a url and i will give back a list of short reviews and long reviews
def get_URL(url):
    Enter_URL=url
    driver.get(Enter_URL)
    element = WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH ,'//*[@id="reviews-medley-footer"]/div[2]/a')))
    element.click()
    strUrl = driver.current_url;
    URL_turn_page= strUrl+ "&pageNumber="
    SR = []
    LR = []
    p=math.ceil(int("".join([i for i in ( driver.find_element_by_xpath('//*[@id="filter-info-section"]/div/span')).text.split("|")[1] if i.isdigit()]))/10)
    print('No. of pages to scrape : ',p)   
    
    for i in tqdm(range(1,p+1)):
        driver.get(URL_turn_page+str(i))

        for j in tqdm(range(1,11)):
            sleep(0.5)
            try:
                if(driver.find_elements_by_xpath("//*[contains(text(), 'From other countries')]")): #for foreign review the path has slight change
                    SR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[2]/span[2]/span').text)
                    LR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[4]/span/span').text)
                else: #for Indian reviews
                    SR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[2]/a[2]/span').text)
                    LR.append(driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[4]/span/span').text)
            except NoSuchElementException:
                continue   
            clear_output(wait=True)
    return SR,LR
    # d = zip(SR,LR)
    # mapped = list(d)
    # df = pd.DataFrame(mapped, columns =['Short_review', 'Long_Review'])
    # return df
    

# url='https://www.amazon.com/HP-15-Athlon-Gold-Bluetooth/dp/B08RCW9PNH/ref=sr_1_1_sspa?dchild=1&keywords=HP%2BPavilion%2B15&qid=1627282296&sr=8-1-spons&smid=AWVDPEZSR45X1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyMFM0UFM2S1pQNkRWJmVuY3J5cHRlZElkPUEwMTY2NDMxMzVJOFBBSEIwQVFIVSZlbmNyeXB0ZWRBZElkPUEwODU3MTMyMlRONk9NMjZHQjFOTiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU&th=1'
# df= get_URL(url)


#Takes a text, searches for different products,find URLS and Product names, 
#find reviews of each URL and returns a SINGLE DF

def get_product_URL(text):
# timeout:exception WebDriverWait(driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'div[data-asin]')))
    meta_URL= text.replace(' ','+')
    mega_URL= f'https://www.amazon.in/s?k={meta_URL}&ref=nb_sb_noss_2'
    print(mega_URL)
    driver.get(mega_URL)
    elements = WebDriverWait(driver,20).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR ,'div[data-asin]')))
    print(len(elements))
    links=[]
    titles=[]
    prices=[]
    S_reviews=[]
    L_reviews=[]
    for i,item in enumerate(elements):    
        link=item.find_element_by_tag_name('a').get_attribute('href')
        SR,LR= get_URL(link)
        
        #Yaha pe driver ko malum nahi chall paa raha hai ki, Driver abhi konse link mai hai
        title=item.find_element_by_tag_name('span').text
        try:
            price= item.find_element_by_class_name('a-price').text
            # print("Elements :",i,title[:10], price)
            links.append(link)
            title.append(title)
            prices.append(price)
            S_reviews.append(SR)
            L_reviews.append(LR)
            if i== len(elements)-1:
                break
            
        except NoSuchElementException:
            print('error',i,' :element not found')
            continue
    df= pd.DataFrame({'Title':titles,'Links':links,'prices':prices,'Short reviews':S_reviews,'Long Reviews':L_reviews})
    return df
    
df= get_product_URL('Best Laptop under 40000')


