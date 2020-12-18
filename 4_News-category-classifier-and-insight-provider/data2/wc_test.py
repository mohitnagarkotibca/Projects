# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 00:18:27 2020

@author: HP
"""
import pandas as pd
import pickle
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import punkt
from nltk.corpus.reader import wordnet
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
from bs4 import BeautifulSoup
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output,State
import plotly.graph_objs as go
import plotly.express as px
import re
import spacy
from spacy.matcher import PhraseMatcher
import numpy as np
from wordcloud import WordCloud
import os
import base64
# nlp=spacy.load('en_core_web_md')
# matcher= PhraseMatcher(nlp.vocab)
# stop_words= list(pd.read_pickle('data/stop_words.pickle'))


# df2= pd.read_csv('data/theasianage.csv',index_col=0)
# df2['newspaper']= 'theasianage'
# df3= pd.read_csv('data/theguardian.csv',index_col=0)
# df3['newspaper']= 'theguardian'
# df4= pd.read_csv('data/themint.csv',index_col=0)
# df4['newspaper']= 'themint'
# df= pd.concat([df2,df3,df4],axis=0).reset_index(drop=True)
# def clean_df(df):
#     def clean(df):
#         df['news_punctuation_cleaned']= df['news'].str.replace('\n+',' ')
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r"\'s","")
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r"[^A-Za-z0-9\s-]",'')
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r"[0-9]+(['a-z']+)?",' ')
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'\s?(-+)\s',' ')
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'\s\s','')
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'-\w[-]\w+','')
#         df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'-',' ')
        
#         df['title_punctuation_cleaned']= df['title'].str.replace('\n+',' ')
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r"\'s","")
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r"[^A-Za-z0-9\s-]",'')
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r"[0-9]+(['a-z']+)?",' ')
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'\s?(-+)\s',' ')
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'\s\s','')
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'-\w[-]\w+','')
#         df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'-',' ')
#         return df

#     df2_feature=clean(df)

#     def lemmatize(df):
#         li=[]
#         for doc in nlp.pipe(df['news_punctuation_cleaned'],disable=['tagger','parser','ner','textcat'],batch_size=4):
#             li.append(' '.join([token.lemma_ for token in doc if token.lemma_ not in stop_words] ))
#         df['lemma_cleaned_news']= li
#         return df
#     df3_feature= lemmatize(df2_feature)
    
#     def convert_to_lower(df):
#         df['news_lower_case']= df['lemma_cleaned_news'].apply(lambda x: x.lower())
#         return df
    
#     df4_feature= convert_to_lower(df3_feature)
#     return df4_feature

# df4_cleaned= clean_df(df)
# model= pd.read_pickle('Models/best_rfc.pickle')
# tf= pd.read_pickle('tfidf.pickle')
# train_x= tf.transform(df['news_lower_case'])
# answer= model.predict(train_x)
# df['predictions']=answer
# df.to_csv('news.csv')
df= pd.read_csv('news.csv').drop('Unnamed: 0',axis=1)


app= dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout= html.Div(
    children=[
        dcc.Dropdown(id='dropdown1',
                      options=[
                          {'label':'politics','value':'politics'},
                          {'label':'business','value':'business'},
                          {'label':'sport','value':'sport'},
                          {'label':'tech','value':'tech'},
                          {'label':'entertainment','value':'entertainment'}
                          ],
                      value='politics',
                      multi=False
                      )
        ,
        html.Div(id='word_cloud1',children=[
            
        ]
        )

        

        ]        
    )



import base64
global selected_val
global list_len

def group_by_val(value):
    df_g= df.groupby('predictions').get_group(value)
    return df_g
def make_popover(i):
    popover= dbc.Popover([
                    dbc.PopoverHeader('somthing'),
                    dbc.PopoverBody('body')
                    ],
                    id='popover_{}'.format(str(i)),
                    target='b_{}'.format(str(i)),
                    placement='bottom')
    return popover
def make_button(i):
    button= dbc.Button('Read More',id='b_{}'.format(str(i)),color='success'),
    return button
    
@app.callback(
    Output(component_id='word_cloud1',component_property='children'),
    [ Input(component_id='dropdown1',component_property='value')]
    )


def make_wordclouds(value):
    selected_val= value
    df_g= group_by_val(value)

    index=df_g.index
    
    length_df= 3
    for num in range(length_df):
        news_titles= df_g['title'].values[num]
        WordCloud(width=400,height=200,contour_color='white').generate(news_titles).to_file('tmp_images/image_{}.png'.format(num))

    images= os.listdir('tmp_images/')
    
    list_length= len(images)
    list_len = list_length
    
    names= [f'card_{num}' for num in range(list_length)]    
    cards=[]
    popovers=html.Div([make_popover(i) for i in range(list_length)]+[make_button(i) for i in range(list_length)])
    
        
    for i in range(list_length):
        image_name=images[i]
        image=base64.b64encode(open('tmp_images/{}'.format(image_name),'rb').read())            
        names[i] = dbc.Card([
            dbc.CardImg(src='data:image/png;base64,{}'.format(image.decode()),top=True, bottom=False,alt='Not working'),
            dbc.CardBody([
                html.H6(f"{df_g['title'].loc[index[i]]}",className='card-title'),
                popovers

                
            ])#--card body
                
                ],outline=True,style={"width": "15rem"}
            )
        cards.append(names[i])
    figs= dbc.Row(
            cards,
            justify='around',
            className="h-35"
        )
    z=[os.remove(f'tmp_images/{im}') for im in images]
    def toggle_popover(n,is_open):    
        if n:
            return not is_open
        return is_open

    for p in [0]:
        app.callback(
            Output('popover_{}'.format(p),'is_open'),
            [Input('b_{}'.format(p),'is_open')],
            [State('popover_{}'.format(p),'is_open')]
            )(toggle_popover)

    return  figs
    

    

app.run_server(debug=True)











app= dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
list_length=10

def toggle_popover(n,is_open):    
    if n:
        return not is_open
    return is_open

def group_by_val(value):
    df_g= df.groupby('predictions').get_group(value)
    return df_g

def make_popover(i):
    popover= dbc.Popover([
                    dbc.PopoverHeader('somthing'),
                    dbc.PopoverBody('body')
                    ],
                    id='popover_{}'.format(str(i)),
                    target='b_{}'.format(str(i)),
                    placement='bottom')
    return popover

def make_button(i):
    button= dbc.Button('Read More',id='b_{}'.format(str(i)),color='success'),
    return button  
  
popovers=html.Div([make_button(i) for i in range(list_length)]+ [make_popover(i) for i in range(list_length)])
app.layout= html.Div([
    popovers
    ])

for p in range(list_length):
    app.callback(
        Output('popover_{}'.format(str(p)),'is_open'),
        [Input('b_{}'.format(str(p)),'is_open')],
        [State('popover_{}'.format(str(p)),'is_open')]
        )(toggle_popover)

app.run_server(debug=False)

