# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 08:30:57 2021

@author: HP
"""

import pickle
import pandas as pd
import nltk
import os
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
import dash_bootstrap_components as dbc
from wordcloud import WordCloud
import base64
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import time
import re
import yake
from Scrappers import scrap_the_hindu,scrap_theasianage,scrap_theguardian,scrap_themint

nlp=spacy.load('en_core_web_md')
matcher= PhraseMatcher(nlp.vocab)
stop_words= list(pd.read_pickle('data/stop_words.pickle'))
model= pd.read_pickle('Models/best_rfc.pickle')
tf= pd.read_pickle('Models/tfidf.pickle')



# df3= scrap_theguardian()
# df1= scrap_the_hindu()
# df2= scrap_theasianage()
# df4= scrap_themint()
df3= pd.read_csv('data/theguardian.csv')
df3['newspaper']= 'theguardian'
df1= pd.read_csv('data/thehindu.csv')
df1['newspaper']= 'thehindu'
df2= pd.read_csv('data/theasianage.csv')
df2['newspaper']= 'theasianage'
df4= pd.read_csv('data/themint.csv')
df4['newspaper']= 'themint'
df= pd.concat([df1,df2,df3,df4],axis=0).reset_index(drop=True)
def clean_df(df):
    def clean(df):
        df['news_punctuation_cleaned']= df['news'].str.replace('\n','')
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r"\'s","")
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r"[^A-Za-z0-9\s-]",'')
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r"[0-9]+(['a-z']+)?",' ')
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'\s?(-+)\s',' ')
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'\s\s','')
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'-\w[-]\w+','')
        df['news_punctuation_cleaned']= df['news_punctuation_cleaned'].str.replace(r'-',' ')
        df['title_punctuation_cleaned']= df['title'].str.replace('\n+',' ')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r"\'s","")
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r"[^A-Za-z0-9\s-]",'')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r"[0-9]+(['a-z']+)?",' ')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'\s?(-+)\s',' ')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'\s\s','')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'-\w[-]\w+','')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace(r'-',' ')
        df['title_punctuation_cleaned']= df['title_punctuation_cleaned'].str.replace('1hr\s','')
        return df
    df2_feature= clean(df)
    def lemmatize(df):
        li=[]
        for doc in nlp.pipe(df['news_punctuation_cleaned'],disable=['tagger','parser','ner','textcat'],batch_size=4):
            li.append(' '.join([token.lemma_ for token in doc if token.lemma_ not in stop_words] ))
        df['lemma_cleaned_news']= li
        return df
    df3_feature= lemmatize(df2_feature)
    def convert_to_lower(df):
        df['news_lower_case']= df['lemma_cleaned_news'].apply(lambda x: x.lower())
        return df
    df4_feature= convert_to_lower(df3_feature)
    return df4_feature
df4_cleaned= clean_df(df)
#-----------------------------------------
dic={}
for line in df4_cleaned['news_punctuation_cleaned']:
    for word in line.split():
        if word in dic.keys():
            dic[word]= dic[word]+1
        else:
            dic[word]= 1

#-----------------------------------------

app= dash.Dash(__name__)
markdown_text1 = '''

This application gathers the latest news from the newspapers **The Hindu**, **The Asian Age**,**'Hindustan Times'** and **The Mint**, predicts their category between **Politics**, **Business**, **Entertainment**, **Sport**, **Tech** and **Other** and then shows a graphic summary.

The news categories are predicted with a Support Vector Machine model.

Please enter which newspapers would you like to scrape news off and the graphs will be loaded **Automatically** :

The scraped news are converted into a numeric feature vector with TF-IDF vectorization. Then, a Support Vector Classifier is applied to predict each category.

'''

def model_predict(df_specific_newspapers):
    feature_vector= tf.transform(df_specific_newspapers['news_lower_case'])
    predictions= model.predict(feature_vector)
    df_specific_newspapers['category']= predictions
    return df_specific_newspapers

#app's Layout
app.layout= dbc.Container([
    html.Br(),
    dbc.Row(
        [
            dbc.Col([ html.H1('Latest News Insight')],
                    style={'background-color':'#f7fcff','text-align':'center'},
                    width={'size':12}
                    )
        ]        
        ),
    html.Br(),
    dbc.Row(
            [
            dbc.Col([dcc.Markdown(markdown_text1)],
                    style={'color':'#ffffff'})
            #printing nouns and adjective
            ]
        ),
    dbc.Row(
        [
        dbc.Col([
            dcc.Dropdown(           
            options=[
                {'label': 'The hindu', 'value': 'thehindu'},
                {'label': 'the guardian', 'value': 'theguardian'},
                {'label': 'The Asian Age', 'value': 'theasianage'},
                {'label': 'The Mint', 'value': 'themint'}
                
            ],
            id='Dropdown_news',
            className= 'dropdown-header',
            placeholder= 'Select News Papers',
            value=['thehindu','theguardian','theasianage','themint'],
            multi=True,
            style={'backgroud-color':'#c5e0f0','height': '30px', 'width': '500px'})
        ],width={'order':1,'offset':3})
        ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='graph1',figure= {})
            ],style={'size':4,'backgroud-color':'#c5e0f0'}),
        dbc.Col([
            dcc.Graph(id='graph2',figure= {})
            ],style={'size':4,'backgroud-color':'#c5e0f0'})
        ]),
    html.Br(),
    dbc.Row([
    dbc.Col([
        dcc.Dropdown(id='dropdown1',
                  options=[
                      {'label':'politics','value':'politics'},
                      {'label':'business','value':'business'},
                      {'label':'sport','value':'sport'},
                      {'label':'tech','value':'tech'},
                      {'label':'entertainment','value':'entertainment'}
                      ],
                  value='politics',
                  multi=False,
                  className='text-left',
                  style={'height': '30px', 'width': '500px','backgroud-color':'#c5e0f0'})
                  ],width={'order':1,'offset':3})  
    
    ]),
    html.Br(),
    dbc.Row([
            
        dbc.Col([
            
            dcc.Loading(children= [html.Div(id='word_cloud1',children=[])],
                    style={'size':7})


        ])
    ])
              
    ],style={'background-color':'#042b41','height': '100%', 'width': '90%'},className='text-monospace',fluid=True
    )

@app.callback(
    Output(component_id='graph1',component_property= 'figure'),
    [Input(component_id='Dropdown_news',component_property='value')]
    )
def update_graph1(values):
    newspaper_list=[]
    counts=[]
    for newspaper in values:
        df4_g= df4_cleaned.groupby('newspaper').get_group(newspaper.strip())
        news_count= df4_g['newspaper'].value_counts()
        z= [newspaper_list.append(newspaper) for newspaper in news_count.index]
        z1= [counts.append(count) for count in news_count.values]
    
    fig= go.Figure(
                    go.Pie(
                    values= counts,
                    labels= newspaper_list,
                    textinfo='label+percent'
                    )
    )
    fig.update_layout(
        {'title':' Article contribution from different newspaper :'}
    )
    return fig

@app.callback(
    Output(component_id='graph2',component_property='figure'),
    [Input(component_id='Dropdown_news',component_property='value')]
    )
def update_graph2(values):
    dfs=[]
    for newspaper in values:
        dfs.append(df.query(f'newspaper== "{newspaper.strip()}"'))
    df_specific_newspapers= pd.concat(dfs,axis=0)
    
    df_specific_newspapers= model_predict(df_specific_newspapers)


    #confuzed between df4_cleaned and df_specific_newspapers
    d_count= df_specific_newspapers['category'].value_counts()

    fig= go.Figure(
        go.Bar(
        x= d_count.index,
        y= d_count.values,
        marker_color= '#ecfaea'
        )
    )
    fig.update_layout(
        plot_bgcolor="#7ab472",
        autosize=False
    )
    for i in range(len(d_count)):
        fig.add_annotation(
        x= d_count.index[i],
        y= d_count.values[i]+5,
        text= '',
        showarrow=False
        )
    for i in range(len(d_count)):
        fig.add_annotation(
        x= d_count.index[i],
        y= d_count.values[i]+5,
        text= str(d_count.values[i]),
        showarrow= False
        )
    fig.update_layout(dict(
    title=" Different category articles which are available",
    xaxis_title="categories",
    yaxis_title="number of articles",
        ))
    return fig

@app.callback(
    Output(component_id='word_cloud1',component_property='children'),
    [ Input(component_id='dropdown1',component_property='value')]
    )

def make_wordclouds(value):
    df_specific_newspapers= model_predict(df4_cleaned)
    
    df_g= df_specific_newspapers.groupby('category').get_group(value)
    index=df_g.index
    for num in range(len(df_g)):
        news_titles= df_g['title_punctuation_cleaned'].values[num]
        WordCloud(width=400,height=200,contour_color='white').generate(news_titles).to_file('tmp_images/image_{}.png'.format(num))

    images= os.listdir('tmp_images/')
    
    list_length= len(images)
    names= [f'card_{num}' for num in range(list_length)]
    
    
    li=[]
    for i in range(list_length):
        image_name=images[i]
        image=base64.b64encode(open('tmp_images/{}'.format(image_name),'rb').read())    
        
        names[i] = dbc.Card([
            dbc.CardImg(src='data:image/png;base64,{}'.format(image.decode()),top=True, bottom=False,alt='Not working'),
            dbc.CardBody([
                html.H6(f"{df_g['title'].loc[index[i]]}",className='card-title'),
                
                dbc.Button('Read More',href=f"{df_g['links'].loc[index[i]]}",target='_blank',color='success')

                ]
                
                
                )],outline=True,style={"width": "15rem"}
            )
        li.append(names[i])
    figs= dbc.Row(
            li,
            justify='around',
            className="h-35"
        )
    z=[os.remove(f'tmp_images/{im}') for im in images]
    
    return  figs

app.run_server(debug=False)
