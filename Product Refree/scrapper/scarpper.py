import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.edge.options import Options
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
from joblib import Parallel,delayed


def get_options():    
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    return options

def get_driver(opt):
    # return Edge(executable_path='../driver/msedgedriver.exe',options = opt)
    return Edge(executable_path=f'{os.getcwd()}/driver/msedgedriver.exe',options = opt)
    

# give me a url and i will give back a list of short reviews and long reviews
class Scrapp:
    def __init__(self,driver):
        self.driver=driver
        self.driver2=None
        
    def get_URL(self,url):
        options= get_options()
        self.driver2 = get_driver(options)
        
        # self.driver.switch_to.frame(0);
        Enter_URL=url
        self.driver2.get(Enter_URL)
        element = WebDriverWait(self.driver2,20).until(EC.visibility_of_any_elements_located((By.XPATH ,'//*[@id="reviews-medley-footer"]/div[2]/a')))
        # print('elements length : ',len(element))
        element[0].click()
        
        strUrl = self.driver2.current_url;
        URL_turn_page= strUrl+ "&pageNumber="
        SR = []
        LR = []
        p=math.ceil(int("".join([i for i in ( self.driver2.find_element_by_xpath('//*[@id="filter-info-section"]/div/span')).text.split("|")[1] if i.isdigit()]))/10)
        if p>8:
            p=8
        print('No. of pages to scrap in the given url : ',p,'\n')   
        # print('-'*20,'\nB :',self.driver2.current_url)
        for i in range(1,p+1):
            print('Turning pages: ',i)
            self.driver2.get(URL_turn_page+str(i))
            for j in tqdm(range(1,11)):
                sleep(0.5)
                try:
                    if(self.driver2.find_elements_by_xpath("//*[contains(text(), 'From other countries')]")): #for foreign review the path has slight change
                        SR.append(self.driver2.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[2]/span[2]/span').text)
                        LR.append(self.driver2.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[4]/span/span').text)
                    else: #for Indian reviews
                        SR.append(self.driver2.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[2]/a[2]/span').text)
                        LR.append(self.driver2.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div['+str(j)+']/div/div/div[4]/span/span').text)
                except NoSuchElementException:
                    continue   
        # print('-'*20,'\nC :',self.driver2.current_url)
        self.driver2.quit()
        return SR,LR
    
        #uncommnet to get a DF(IF NEEDED : TIME= BIG
        # d = zip(SR,LR)
        # mapped = list(d)
        # df = pd.DataFrame(mapped, columns =['Short_review', 'Long_Review'])
        # return df
           
    
    
    #Takes a text, searches for different products,find URLS and Product names, 
    #find reviews of each URL and returns a SINGLE DF
    def get_best_product(self,text):
    # timeout:exception WebDriverWait(self.driver,20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR ,'div[data-asin]')))
        meta_URL= text.replace(' ','+')
        mega_URL= f'https://www.amazon.in/s?k={meta_URL}&ref=nb_sb_noss_2'
        self.driver.get(mega_URL)
        elements = WebDriverWait(self.driver,20).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR ,'div[data-asin]')))
        links=[]
        titles=[]
        prices=[]
        S_reviews=[]
        L_reviews=[]
        
        for i,item in enumerate(elements[3:7]):    
            print('-'*10,'item number :',i,'-'*10)
            link=item.find_element_by_tag_name('a').get_attribute('href')
            # print('-'*20,'\nA: ',self.driver.current_url) --for debug
            SR,LR= self.get_URL(link)
            # self.driver.switch_to.parent_frame();

            # print('-'*20,'\nD: ',self.driver.current_url) --debug
            

            title=item.find_element_by_tag_name('span').text
            try:
                price= item.find_element_by_class_name('a-price').text
                # print("Elements :",i,title[:10], price)
                
                links.append(link)
                titles.append(title)
                prices.append(price)
                S_reviews.append(SR)
                L_reviews.append(LR)
                if i== len(elements)-1:
                    break
                
            except NoSuchElementException:
                print('error',i,' :element not found')
                continue
            print('item num :',i,' completed')
        df= pd.DataFrame({'Title':titles,'Links':links,'prices':prices,'Short reviews':S_reviews,'Long Reviews':L_reviews})
        return df


def scrap_obj(text):
    opt= get_options()
    driver = get_driver(opt)
    SC= Scrapp(driver)
    return SC.get_best_product(text)
# df.to_csv('1st_scrap.csv')
